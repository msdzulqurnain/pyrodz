from framework.route import Route
from app.Support.Filters import private

from app.Handlers.StartHandler import StartHandler
from app.Handlers.SearchHandler import SearchHandler


Route.inline(SearchHandler.inline)
Route.current(SearchHandler.current)

# commands
Route.command("start", StartHandler.start, private)
