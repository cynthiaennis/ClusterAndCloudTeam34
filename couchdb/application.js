{
    "language": "javascript",
    "views": {
        "location_count_positive": {
            "map": "function(doc) { if ( doc.user.location && doc.positive) { if (doc.positive == true) { emit(doc.user.location, 1); } } }",
            "reduce":"_count"
        },
	"location_count_all": {
            "map": "function(doc) { if ( doc.user.location ){ emit(doc.user.location, 1); } }",
	    "reduce":"_count"
        }
    }
}