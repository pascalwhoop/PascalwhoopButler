class MercuryResponse(object):

    def __init__(
            self,
            title           = None,
            content         = None,
            author          = None,
            date_published  = None,
            lead_image_url  = None,
            dek             = None,
            next_page_url   = None,
            url             = None,
            domain          = None,
            excerpt         = None,
            word_count      = None,
            direction       = None,
            total_pages     = None,
            rendered_pages  = None,
    ):
        self.title          = title
        self.content        = content
        self.author         = author
        self.date_published = date_published
        self.lead_image_url = lead_image_url
        self.dek            = dek
        self.next_page_url  = next_page_url
        self.url            = url
        self.domain         = domain
        self.excerpt        = excerpt
        self.word_count     = word_count
        self.direction      = direction
        self.total_pages    = total_pages
        self.rendered_pages = rendered_pages
