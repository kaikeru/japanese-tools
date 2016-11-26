var config = {
    context: {
        // Social Context
        social: {
            twitter: process.env.TWITTER || "twitterName",
            facebook: process.env.FACEBOOK || "facebookname"
        }
    },
    database: {
        host: process.env.MONGO_HOST || process.env.IP || "localhost"
    }
}

module.exports = config;
