TEMPLATE = """
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:googleplay="http://www.google.com/schemas/play-podcasts/1.0" xmlns:media="http://www.rssboard.org/media-rss" version="2.0">
    <channel>
        <title>{{title}}</title>
        <link>{{base_url}}</link>
        <language>{{language}}</language>
        <atom:link href="{{xml_link}}" rel="self" type="application/rss+xml"/>
        <copyright>{{copyright}}</copyright>
        <itunes:subtitle>{{subtitle}}</itunes:subtitle>
        <itunes:author>{{author}}</itunes:author>
        <itunes:summary>
        {{description}}
        </itunes:summary>
        <itunes:keywords>
        Machine Learning, Natural Language Processing, Artificial Intelligence
        </itunes:keywords>
        <description>
        {{description}}
        </description>
        <itunes:owner>
        <itunes:name>{{author}}</itunes:name>
        <itunes:email>{{email}}</itunes:email>
        </itunes:owner>
        <itunes:image href="{{cover_path}}"/>
        {% for category in categories %}
        <itunes:category text="{{category}}"></itunes:category>
        {% endfor %}

        {% for episode in episode_meta %}
        <item>
        <title>{{episode['title']}}</title>
        <itunes:title>{{episode['title']}}</itunes:title>
        <itunes:author>Gabriel Simmons</itunes:author>
        <itunes:subtitle>
        {{episode['subtitle']}}
        </itunes:subtitle>
        <itunes:summary>
        <![CDATA[
        {{episode['description']}}
        ]]>
        </itunes:summary>
        <description>
        <![CDATA[
        {{episode['description']}}
        ]]>
        </description>
        % <itunes:image href="https://OPTIONAL EPISODE IMAGE.jpg"/>
        <enclosure url="{{episode['mp3path']}}" length="{{episode['length']}}" type="audio/mpeg"/>
        <itunes:duration>{{episode['duration']}}</itunes:duration>
        <itunes:season>{{episode['season']}}</itunes:season>
        <itunes:episode>{{episode['episode_number']}}</itunes:episode>
        <itunes:episodeType>full</itunes:episodeType>
        <guid isPermaLink="false">
        {{episode['mp3path']}}
        }}</guid>
        <pubDate>{{episode['publish_date']}}</pubDate>
        <itunes:explicit>NO</itunes:explicit>
        </item>
        {% endfor %}

    </channel>
</rss>
"""
