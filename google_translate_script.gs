//replace "XXXXXXXX" with the folder name for files you want to translate into English
function runTranslation() {
  var folder_id = getFolderID("XXXXXXXX");
  var folder = DriveApp.getFolderById(folder_id);
  var contents = folder.getFiles();
  while (contents.hasNext()) {
   var content = contents.next();
   var file_id = content.getId();
   translateText(file_id);
 }
}

function getFolderID(fname){
  var folders = DriveApp.getFolders();
  while (folders.hasNext()) {
   var folder = folders.next();
   if(folder.getName() == fname){
    return folder.getId();
   }
 }
}

function translateText(file_id) {
  var text = DocumentApp.openById(file_id).getBody().getText();
  var x = LanguageApp.translate(text, '', 'en');
  insertText(file_id, x);
}

function insertText(file_id, newText) {
  var selection = DocumentApp.openById(file_id).getBody();
  selection.clear();
  selection.asText().setText(newText);

}
