import logging

from PySide2.QtCore import QDir, QFile, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtSql import QSqlDatabase

from sqlDialog import SqlConversationModel

logging.basicConfig(filename="chat.log", level=logging.DEBUG)
logger = logging.getLogger("logger")

def connectToDatabase():
    database = QSqlDatabase.database()
    if not database.isValid():
        database = QSqlDatabase.addDatabase("QSQLITE")
        if not database.isValid():
            logger.error("Cannot add database")

    write_dir = QDir()
    if not write_dir.mkpath("."):
        logger.error("Failed to create writable directory")

    # Ensure that we have a writable location on all devices.
    filename = "{}/chat-database.sqlite3".format(write_dir.absolutePath())

    # When using the SQLite driver, open() will create the SQLite
    # database if it doesn't exist.
    database.setDatabaseName(filename)
    if not database.open():
        logger.error("Cannot open database")
        QFile.remove(filename)

if __name__ == "__main__":
    app = QGuiApplication()
    connectToDatabase()
    sql_conversation_model = SqlConversationModel()

    engine = QQmlApplicationEngine()
    # Export pertinent objects to QML
    engine.rootContext().setContextProperty("chat_model", sql_conversation_model)
    engine.load(QUrl("chat.qml"))

    app.exec_()