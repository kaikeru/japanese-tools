var config = {
    context: {
        // Social Context
        social: {
            twitter: process.env.TWITTER || "twitterName",
            facebook: process.env.FACEBOOK || "facebookname"
        },
        google: {
            analyticsID: process.env.GOOGLE_ANALYTICS_ID
        }
    },
    mongodb: {
        uri: process.env.MONGODB_URI || process.env.IP || "localhost"
    }
}

module.exports = config;
