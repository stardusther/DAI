# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory to /frontend
WORKDIR /frontend

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Bundle app source
COPY . .

# Expose port 4200 to the outside world
EXPOSE 4200

# Run npm start when the container launches
CMD ["npm", "start"]
