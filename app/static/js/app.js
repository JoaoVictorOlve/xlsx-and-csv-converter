let filenameLabel = document.getElementById("formFileLg")
let selectedFile = document.getElementById("selectedFile")
let convertBtn = document.getElementById("convert-btn")

async function getFileData(myFile){
    var data = new FormData()
    data.append('file', myFile.files[0])
    await fetch('/verify_file',{
        method: 'POST',
        body: data,
    }).then(res=>{
        if(res.status == 200){
            filename = myFile.files[0].name
            filenameLabel.innerText = filename;
            convertBtn.style = "display:block";
            if (filename.split('.').pop() == "xlsx"){
                convertBtn.innerText = "Convert to CSV"
            } else {
                convertBtn.innerText = "Convert to XLSX"
            }
        } else {
            location.reload();
            selectedFile.value = "";
            filenameLabel.innerText = "";
            convertBtn.style = "display:none";
        }
    })

}