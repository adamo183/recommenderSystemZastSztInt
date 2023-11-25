const batchTrack = document.getElementById("movieSelect");
let displayList = [];

const getPost = async () => {
    const response = await fetch("http://127.0.0.1:8000/films");
    const data = response.json();
    return data;
};

const getRecommendation = async (film) => {
    const response = await fetch("http://127.0.0.1:8000/recommend/movie/name/"+film);
    const data = response.json();
    return data;
};

const displayOption = async () => {
    const options = await getPost();
    const obj = JSON.parse(options)
    const newOption = document.createElement("option");
    newOption.value = '';
    newOption.text = '';
    batchTrack.appendChild(newOption);

    for(var i in obj)
    {
        const newOption = document.createElement("option");
        newOption.value = obj [i];
        newOption.text = obj [i];
        batchTrack.appendChild(newOption);
    }
};

document.getElementById('movieSelect').onchange =  async (value) =>{
    const filmToRecomment = value.target.value;
    if(filmToRecomment != ''){
        const response = await getRecommendation(filmToRecomment);
        
        console.log(JSON.stringify(response.recomendation.Series_Title))
        if (JSON.stringify(response.recomendation.Series_Title).length>0)
        {
            document.getElementById("recomendation_label").style.visibility = 'visible';
        }
        else
        {
            document.getElementById("recomendation_label").style.visibility = 'hidden';
        }

        var list = document.getElementById("recomendation");
        document.getElementById("recomendation").innerHTML = "";
        for(var item in response.recomendation.Series_Title)
        {
            displayList.push(response.recomendation.Series_Title[item]);
            let li = document.createElement("li");
            li.innerText = response.recomendation.Series_Title[item];
            list.appendChild(li);
        }
    }
};

displayOption();