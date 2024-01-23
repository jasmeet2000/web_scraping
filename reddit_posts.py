import scrapy

class RedditPostsSpider(scrapy.Spider):
    name            = 'reddit_posts'
    allowed_domains = ['old.reddit.com']
    start_urls      = ['https://old.reddit.com/r/datascience/']

    def parse(self, response):
        for post in response.css('div.thing'):
            item = {
                'title'        : post.css('a.title::text').get(),
                'post_by'      : post.css('a.author::text').get(),
                'sub_reddit'   : response.url.split('/')[4],
                'created_at'   : post.css('time::attr(title)').get(),
                'total_comment': post.css('a.bylink::text').get(),
            }

            # Extract the post URL
            post_url = post.css('a.title::attr(href)').get()
            
            # Follow the post URL to scrape the entire post
            yield response.follow(post_url, self.parse_post, meta={'item': item})

        # Follow the "next" link to paginate through posts
        next_page = response.css('span.next-button a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        item = response.meta['item']
        
        # Extract the initial post content
        initial_post         = response.css('div.expando p::text').getall()
        item['initial_post'] = ' '.join(initial_post)
        
        # Extract comments
        comments = []
        for comment in response.css('div.commentarea div.comment'):
            comment_text  = comment.css('div.entry form div.usertext-body p::text').getall()
            comments.append('|'.join(comment_text))
        
        #item['comments'] = comments

        yield item
