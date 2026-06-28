from framework.route import Route
from app.Support.Filters import private, text

from app.Handlers.StartHandler import StartHandler
from app.Handlers.SearchHandler import SearchHandler
from app.Handlers.MessageHandler import MessageHandler


Route.inline(SearchHandler.inline)
Route.current(SearchHandler.current)

# commands
Route.command("start", StartHandler.start, private)
Route.message(MessageHandler.message)
