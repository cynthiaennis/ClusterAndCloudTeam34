{
    "language": "javascript",
    "views": {
        "location_count_positive": {
            "map": "function(doc) { if ( doc.tweet.tweet_location && doc.tweet.is_negative_sentiment) { if (doc.tweet.is_negative_sentiment == 1) { emit(doc.tweet.tweet_location, 1); } } }",
            "reduce":"_count"
        },
	"location_count_all": {
            "map": "function(doc) { if ( doc.tweet.tweet_location ){ emit(doc.tweet.tweet_location, 1); } }",
	    "reduce":"_count"
        }
    }
}
