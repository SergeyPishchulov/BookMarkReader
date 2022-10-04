//Register the reader events and get reader controller object ( note that these are just callbacks you can't treat them as events though )

var exControls = TreineticEpubReader.handler();
exControls.registerEvent("onEpubLoadSuccess", function () {

});

exControls.registerEvent("onEpubLoadFail", function () {

});

exControls.registerEvent("onTOCLoaded", function (hasTOC) {
    if (!hasTOC) {
       let toc =  exControls.getTOCJson();
    }
    // you can use following api calls after this
    /**
    exControls.hasNextPage()
    exControls.nextPage();
    exControls.hasPrevPage()
    exControls.prevPage();
    exControls.makeBookMark();
    exControls.changeFontSize(int);
    exControls.changeColumnMaxWidth(int);
    exControls.setTheme("theme-id-goes-here");
    exControls.setScrollMode("scroll-type-id-goes-here");
    exControls.setDisplayFormat("display-format-id-goes-here");

    extcontrols.getRecommendedFontSizeRange()
    extcontrols.getRecommendedColumnWidthRange()
    var list = extcontrols.getAvailableThemes();
    var list = extcontrols.getAvailableScrollModes();
    var list = extcontrols.getAvailableDisplayFormats();
    var settings = extcontrols.getCurrentReaderSettings();
    **/
});


// You can feed epub file as well as extracted path of the epub
// if you are planning to use epub file directly make sure that worker js files inside `ZIPJS` the `dist` is copied outside to a accessible location.
// and set the root folder path of those files to 'jsLibRoot'
var config = TreineticEpubReader.config();
config.jsLibRoot = "src/ZIPJS/";

TreineticEpubReader.create("#epub-reader-frame");
TreineticEpubReader.open("assets/epub/epub_1.epub");

To see a code sample open `sample` folder inside the `dist`