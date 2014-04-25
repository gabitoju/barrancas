
class Page():

    def __init__(self, title, content, url, date):
        self.title = title
        self.content = content
        self.url = url
        self.date = date

    @property
    def title(self):
        return self.title

    @setter
    def title(self, title):
        self.title = title

    @property
    def content(self):
        return self.content

    @setter
    def content(self, content):
        self.content = content

    @property
    def url(self):
        return self.url

    @setter
    def url(self, url):
        self.url = url

    @property
    def date(self):
        return self.date

    @setter
    def date(self, date):
        return self.date

	def __lt__(self, obj):
		return self.date < obj.date

	def __le__(self, obj):
		return self.date <= obj.date

	def __eq__(self, obj):
		return self.title == obj.title

	def __ne__(self, obj):
		return self.title != obj.title

	def __gt__(self, obj):
		return self.date > obj.date

	def __ge__(self, obj):
		return self.date >= obj.date
