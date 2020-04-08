require 'json'
require 'redis'
require 'rubygems'
require 'sinatra'

class App < Sinatra::Application

    redis = Redis.new(:host => 'db', :port => '6379')

    set :bind, '0.0.0.0'

    get '/' do
        '<h1>DockerBook Test Redis-eabled Sinatra app</h1>'
    end

    get '/json' do
        params = redis.get 'params'
        params.to_json
    end

    post '/json/?' do
        redis.set 'params', [params].to_json
        params.to_json
    end
end
