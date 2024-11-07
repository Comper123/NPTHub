Dropzone.autoDiscover=false;
const myDropzone= new Dropzone('#dropzone',{
    url:'/',
    paramName: "files",
    maxFiles: 10,
    maxFilesize:2,
    acceptedFiles:'.jpg, .png, .bmp, .psd, .jpeg',
})