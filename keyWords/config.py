import configparser

class ConfigLoader:
    def __init__(self):
        self.keywords, self.similar_keywords = self.load_keywords()

    def load_keywords(self):
        config = configparser.ConfigParser()
        config.read('keywords.ini', encoding="utf-8")

        similar_keywords = {}
        keywords = {}

        for category in config.sections():
            similar_keywords = {}
            keywords_str = config[category]['keywords']
            keywords_list = keywords_str.split(',')

            processed_keywords = []
            for keyword in keywords_list:
                if '（' in keyword:
                    main_keyword = keyword.split('（')[0]
                    similars = keyword.split('（')[1].replace('）', '').split('、')
                    similar_keywords[main_keyword] = similars
                    processed_keywords.append(main_keyword)
                else:
                    processed_keywords.append(keyword)

            keywords[category] = processed_keywords
            similar_keywords[category] = similar_keywords

        return keywords, similar_keywords
