// index.js

import { ApolloServer } from '@apollo/server'
import { startStandaloneServer } from '@apollo/server/standalone'

const typeDefs = `#graphql
    type Query {
        qqq: String
    }
`

const resolvers = {
    Query: {
        qqq: () => {
            return "zxcvㅁㄴㅇㄹㅁㄴㅇㄹㅁㄴㅇㄹzxvzxㄴ"
        }
    }
}

const server = new ApolloServer({
    typeDefs: typeDefs,
    resolvers: resolvers
})

startStandaloneServer(server) // 4000