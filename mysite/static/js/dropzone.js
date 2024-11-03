Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#my-dropzone',{
    url:'create_project/',
    maxFiles:10,
    acceptedFiles:'*.jpg, *.png',
})