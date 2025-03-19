from contextlib import contextmanager, asynccontextmanager
from sqlalchemy import create_engine, event, Pool, text, NullPool
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .config import DatabaseConfig


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        """
        Choose the appropriate engine based on an optional force flag,
        the SQL clause's type and execution options, and the transaction state.
        """
        write_engine = self.info.get("write_engine")
        read_engine = self.info.get("read_engine")

        # First, check if the session has been forced to a specific mode.
        force = self.info.get("force")
        if force == "write":
            return write_engine
        elif force == "read":
            return read_engine

        if clause is not None:
            # Allow execution options on the clause to force a particular engine.
            exec_options = getattr(clause, "get_execution_options", lambda: {})()
            if exec_options.get("force_write", False):
                return write_engine
            if exec_options.get("force_read", False):
                return read_engine

            # Determine engine based on the clause type.
            visit_name = getattr(clause, "__visit_name__", None)
            if visit_name == "select":
                return read_engine
            elif visit_name == "text":
                clause_str = str(clause).strip().lower()
                if clause_str.startswith("select"):
                    return read_engine
            # For all other clauses (INSERT, UPDATE, DELETE, etc.) use the write engine.
            return write_engine

        # If no clause is provided (ORM usage), check if the session is in a transaction.
        if self.in_transaction():
            return write_engine
        return read_engine


class AsyncRoutingSession(AsyncSession):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        """
        Asynchronous version of get_bind() that uses the same logic as its synchronous counterpart.
        """
        write_engine = self.info.get("write_engine")
        read_engine = self.info.get("read_engine")

        force = self.info.get("force")
        if force == "write":
            return write_engine
        elif force == "read":
            return read_engine

        if clause is not None:
            exec_options = getattr(clause, "get_execution_options", lambda: {})()
            if exec_options.get("force_write", False):
                return write_engine
            if exec_options.get("force_read", False):
                return read_engine

            visit_name = getattr(clause, "__visit_name__", None)
            if visit_name == "select":
                return read_engine
            elif visit_name == "text":
                clause_str = str(clause).strip().lower()
                if clause_str.startswith("select"):
                    return read_engine
            return write_engine

        if self.in_transaction():
            return write_engine
        return read_engine


class DatabaseInstance:
    def __init__(self, config: DatabaseConfig):
        self.db_user = config.get('db_user')
        self.db_password = config.get('db_password')
        self.db_host_write = config.get('db_host')
        self.db_host_read = config.get('db_host_read') or self.db_host_write
        self.db_port = config.get('db_port')
        self.db_name = config.get('db_name')
        self.db_ssl = config.get('db_ssl', False)
        self.db_pool_size = config.get('db_pool_size', None)
        self.db_max_overflow = config.get('db_max_overflow', 0)

        self.active_connections = 0

        # Build connection URLs for sync and async for both write and read.
        self.database_path_write = self._build_database_url(async_mode=False, host=self.db_host_write)
        self.database_path_read = self._build_database_url(async_mode=False, host=self.db_host_read)
        self.async_database_path_write = self._build_database_url(async_mode=True, host=self.db_host_write)
        self.async_database_path_read = self._build_database_url(async_mode=True, host=self.db_host_read)

        # Database settings
        db_settings = self._initialize_db_settings()

        # Create synchronous engines for write and read.
        self.engine_write = create_engine(self.database_path_write, **db_settings)
        self.engine_read = create_engine(self.database_path_read, **db_settings)
        # Create a scoped session using our custom RoutingSession.
        # The session’s "info" dict passes both engines.
        self.scoped_session = scoped_session(sessionmaker(
            class_=RoutingSession,
            autocommit=False,
            autoflush=False,
            bind=self.engine_write,  # fallback binding
            expire_on_commit=True,
            info={"write_engine": self.engine_write, "read_engine": self.engine_read}
        ))

        # Create asynchronous engines for write and read.
        self.async_engine_write = create_async_engine(self.async_database_path_write, **db_settings)
        self.async_engine_read = create_async_engine(self.async_database_path_read, **db_settings)
        self.async_session_maker = async_sessionmaker(
            class_=AsyncRoutingSession,
            bind=self.async_engine_write,  # fallback binding
            expire_on_commit=True,
            autocommit=False,
            autoflush=False,
            info={"write_engine": self.async_engine_write, "read_engine": self.async_engine_read}
        )

        # Declarative base for ORM models
        self.base = declarative_base(name="Base")

    def _build_database_url(self, async_mode=False, host=None):
        if host is None:
            host = self.db_host_write
        scheme = "postgresql+asyncpg" if async_mode else "postgresql"
        url = f"{scheme}://{self.db_user}:{self.db_password}@{host}:{self.db_port}/{self.db_name}"
        if self.db_ssl:
            url += "?ssl=require" if async_mode else "?sslmode=require"
        return url

    def _initialize_db_settings(self):
        db_settings = {"pool_pre_ping": True, "echo": False}

        if self.db_pool_size:
            db_settings.update({
                "pool_size": self.db_pool_size,
                "pool_recycle": 300,
                "pool_use_lifo": True,
                "max_overflow": self.db_max_overflow,
            })
        else:
            db_settings["poolclass"] = NullPool

        return db_settings

    def session_local(self):
        return self.scoped_session()

    def get_db(self, force: str = None):
        db = self.session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @contextmanager
    def get_db_cm(self, force: str = None):
        db = self.session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get_clean_db(self, force: str = None):
        db = self.session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.expunge_all()
            db.close()

    @contextmanager
    def get_clean_db_cm(self, force: str = None):
        db = self.session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.expunge_all()
            db.close()

    def get_db_read(self):
        yield from self.get_db(force="read")

    def get_db_write(self):
        yield from self.get_db(force="write")

    @contextmanager
    def get_db_cm_read(self):
        return self.get_db_cm(force="read")

    @contextmanager
    def get_db_cm_write(self):
        return self.get_db_cm(force="write")

    def get_clean_db_read(self):
        yield from self.get_clean_db(force="read")

    def get_clean_db_write(self):
        yield from self.get_clean_db(force="write")

    @contextmanager
    def get_clean_db_cm_read(self):
        return self.get_clean_db_cm(force="read")

    @contextmanager
    def get_clean_db_cm_write(self):
        return self.get_clean_db_cm(force="write")

    def create_tables(self):
        self.base.metadata.create_all(self.engine_write)

    def close_all_connections(self):
        self.engine_write.dispose()
        self.engine_read.dispose()
        print("All connections closed gracefully.")

    def setup_connection_monitoring(self):
        @event.listens_for(Pool, "connect")
        def connect_listener(dbapi_connection, connection_record):
            self.active_connections += 1
            print(f"New database connection created. Total active connections: {self.active_connections}")

        @event.listens_for(Pool, "close")
        def close_listener(dbapi_connection, connection_record):
            self.active_connections -= 1
            print(f"A database connection closed. Total active connections: {self.active_connections}")

    def check_database_health(self):
        try:
            with self.engine_write.connect() as connection:
                connection.execute(text("SELECT 1"))

            with self.engine_read.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False

    def async_session_local(self):
        return self.async_session_maker()

    async def async_get_db(self, force: str = None):
        db = self.async_session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

    async def async_get_clean_db(self, force: str = None):
        db = self.async_session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            db.expunge_all()
            await db.close()

    @asynccontextmanager
    async def async_get_db_cm(self, force: str = None):
        db = self.async_session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

    @asynccontextmanager
    async def async_get_clean_db_cm(self, force: str = None):
        db = self.async_session_local()
        if force in ("read", "write"):
            db.info['force'] = force
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            db.expunge_all()
            await db.close()

    async def async_get_db_read(self):
        async for db in self.async_get_db(force="read"):
            yield db

    async def async_get_db_write(self):
        async for db in self.async_get_db(force="write"):
            yield db

    @asynccontextmanager
    async def async_get_db_cm_read(self):
        return self.async_get_db_cm(force="read")

    @asynccontextmanager
    async def async_get_db_cm_write(self):
        return self.async_get_db_cm(force="write")

    async def async_get_clean_db_read(self):
        async for db in self.async_get_clean_db(force="read"):
            yield db

    async def async_get_clean_db_write(self):
        async for db in self.async_get_clean_db(force="write"):
            yield db

    @asynccontextmanager
    async def async_get_clean_db_cm_read(self):
        return self.async_get_clean_db_cm(force="read")

    @asynccontextmanager
    async def async_get_clean_db_cm_write(self):
        return self.async_get_clean_db_cm(force="write")
