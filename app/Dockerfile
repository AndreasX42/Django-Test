FROM node:20

EXPOSE 4200

WORKDIR /app

COPY ./ ./

RUN npm install

RUN npm install -g @angular/cli

RUN ng analytics off

ENTRYPOINT ["sh", "-c", "ng serve --host 0.0.0.0 --poll 2000"]