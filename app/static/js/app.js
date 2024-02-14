let filenameLabel = document.getElementById("formFileLg")

async function getFileData(myFile){
    var data = new FormData()
    data.append('file', myFile.files[0])
    await fetch('/verify_file',{
        method: 'POST',
        body: data,
    }).then(res=>{
        if(res.status == 200){
            filenameLabel.innerText = myFile.files[0].name
        }
    })

    
}