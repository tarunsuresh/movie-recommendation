from flask import Flask,jsonify,request
import csv 
from demographic import output
import itertools
from content_filtering import get_recommendations


liked_movies=[]
not_liked_movies=[]
did_not_watch=[]

app=Flask(__name__)

@app.route("/get-movie")
def get_movie():
    return jsonify({
        "data":all_movies[0:10],
        "status":"success"
    })

@app.route("/get-liked-movie")
def get_liked_movie():
    return jsonify({
        "data":liked_movies[0],
        "status":"success"
    })
@app.route("/get-disliked-movie")
def get_disliked_movie():
    return jsonify({
        "data":liked_movies[0],
        "status":"success"
    })

@app.route("/popular-movies")
def popular_movies():
    movie_data=[]
    for movie in output:
        d={
            "title":movie[0],
            "poster_link":movie[1],
            "release_data":movie[2],
            "duration":movie[3],
            "rating":movie[4],
            "overview":movie[5]
        }
        movie_data.append(d)
    return jsonify({"data":movie_data,"status":"success"}),200

@app.route("/recommended-movies")
def recommended_movie():
    all_recommended=[]
    for liked_movie in liked_movies:
        output= get_recommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    all_recommended.sort()
    all_recommended=list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data=[]
    for recommended in all_recommended:
        d={
            "title":recommended[0],
            "poster_link":recommended[1],
            "release_data":recommended[2] or "N/A",
            "duration":recommended[3],
            "rating":recommended[4],
            "overview":recommended[5]
        }
        movie_data.append(d)
    return jsonify({
        "data":"movie_data",
        "status":"success"
    }),200


@app.route("/liked-movie",methods=["POST"])
def liked_movie():
    global all_movies
    movie=all_movies[0]
    all_movies=all_movies[1:]
    liked_movies.append(movie)
    return jsonify({
        "status":"success"
    })
@app.route("/disliked-movie",methods=["POST"])
def disliked_movie():
    global all_movies
    movie=all_movies[0]
    all_movies=all_movies[1:]
    not_liked_movies.append(movie)
    return jsonify({
        "status":"success"
    })



if __name__=="__main__":
    app.run()




