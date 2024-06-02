from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].round(2).values)
                           )

@app.route("/recommend")
def recommend_ui():
    return render_template('recommend.html')


@app.route("/recommend_books")
def recommend():
    book_name = request.args.get('user_input')
    print(book_name)
    book_id = np.where(pt.index==book_name)[0]
    if len(book_id) > 0:
        # print(book_id)
        distances , suggestions = model.kneighbors(pt.iloc[book_id,:].values.reshape(1,-1),n_neighbors=10)
        res = []
        for i in range(len(suggestions[0])):
            item = []
            if(i!=0):
                temp_df = books[books["Book-Title"] == pt.index[suggestions[0][i]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                res.append(item)
    else:
        res = ["Book not found"]

    return render_template('recommend.html',data=res)

if __name__ == '__main__':
    app.run(debug=True)