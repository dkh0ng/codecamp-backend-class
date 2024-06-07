FROM node:14

# Create app directory
WORKDIR /myfolder

# Install app dependencies
COPY package.json yarn.lock ./
RUN yarn install

# Install nodemon globally
RUN yarn global add nodemon

# Bundle app source
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Start the app
CMD ["nodemon", "index.js"]
