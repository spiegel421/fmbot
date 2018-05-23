DOWNLOAD_DELAY = 10
CONCURRENT_REQUESTS = 1
ROBOTSTXT_OBEY = False
REDIRECT_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
ITEM_PIPELINES = {
    'lastfm_test.pipelines.CsvPipeline': 500,
    }
