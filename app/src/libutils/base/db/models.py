from sqlalchemy import Table
from libutils.base.db.connection import SqlAlchemyConnection


class ConfigTemplate(SqlAlchemyConnection.base):
    __table__ = Table('config_template', SqlAlchemyConnection.meta, autoload=True)


class ConfigTemplateVersion(SqlAlchemyConnection.base):
    __table__ = Table('config_template_version', SqlAlchemyConnection.meta, autoload=True)


class ConfigVariable(SqlAlchemyConnection.base):
    __table__ = Table('config_variable', SqlAlchemyConnection.meta, autoload=True)


class EdgeConfigVariable(SqlAlchemyConnection.base):
    __table__ = Table('edge_config_variable', SqlAlchemyConnection.meta, autoload=True)


class EdgePackage(SqlAlchemyConnection.base):
    __table__ = Table('edge_package', SqlAlchemyConnection.meta, autoload=True)


class EdgeType(SqlAlchemyConnection.base):
    __table__ = Table('edge_type', SqlAlchemyConnection.meta, autoload=True)


class MasterPackage(SqlAlchemyConnection.base):
    __table__ = Table('master_package', SqlAlchemyConnection.meta, autoload=True)


class MasterPackageConfigTemplate(SqlAlchemyConnection.base):
    __table__ = Table('master_package_config_template', SqlAlchemyConnection.meta, autoload=True)


class TemplateConfigVariable(SqlAlchemyConnection.base):
    __table__ = Table('template_config_variable', SqlAlchemyConnection.meta, autoload=True)


class TemplateSetVersion(SqlAlchemyConnection.base):
    __table__ = Table('template_set_version', SqlAlchemyConnection.meta, autoload=True)


class SwitchPackage(SqlAlchemyConnection.base):
    __table__ = Table('switch_package', SqlAlchemyConnection.meta, autoload=True)


class EdgeTelemetryCode(SqlAlchemyConnection.base):
    __table__ = Table('edge_telemetry_code', SqlAlchemyConnection.meta, autoload=True)


class EdgeTelemetryInfo(SqlAlchemyConnection.base):
    __table__ = Table('edge_telemetry_info', SqlAlchemyConnection.meta, autoload=True)
