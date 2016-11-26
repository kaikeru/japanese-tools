var config = {
    context: {
        // Social Context
        social: {
            twitter: process.env.TWITTER || "twitterName",
            facebook: process.env.FACEBOOK || "facebookname"
        }
    },
    mongodb: {
        uri: process.env.MONGODB_URI || process.env.IP || "localhost"
    }
}

module.exports = config;
