class DataMixin:
    title_page = None
    
    def get_context_data(self):
        context = super().get_context_data()
        if not self.title_page:
            context['title_page'] = self.title_page