from framework import private
from framework.route import Route

from app.Handlers.StartHandler import StartHandler
from app.Handlers.MessageHandler import MessageHandler


# commands
Route.command("start", StartHandler.start, private)
Route.message(MessageHandler.message, private)