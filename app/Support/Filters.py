class FilterProxy:
    def __init__(self, expr):
        self.expr = expr

    def __and__(self, other):
        return FilterProxy(("and", self, other))

    def __or__(self, other):
        return FilterProxy(("or", self, other))

    def __invert__(self):
        return FilterProxy(("not", self))


private = FilterProxy("private")
group = FilterProxy("group")
supergroup = FilterProxy("supergroup")
text = FilterProxy("text")
photo = FilterProxy("photo")
video = FilterProxy("video")
document = FilterProxy("document")