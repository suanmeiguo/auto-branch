FROM ruby:2.6.3

COPY ./app /app
WORKDIR /app
ENV PYTHONENV /app

RUN gem install bundler
RUN bundle install

Expose 5000

CMD ruby server.rb
