// ----------------------------------------------------------------------------
// CzechTile set for MarkItUp!
//
// Based on example wiki set (http://markitup.jaysalvat.com/examples/wiki/)
// ----------------------------------------------------------------------------
CTTASettings = {
    nameSpace:          "ctta",
    previewParserPath:  "",  // FIXME?
    previewParserVar:   "text",
    onCtrlEnter:       { keepDefault: false,
        replaceWith: '\n\n' },
    onShiftEnter:      { keepDefault: false,
        replaceWith: function (markitup) { return lac.append(markitup); } },
    markupSet:  [
        { name: 'Nadpis 1', className: 'h1', key:'1',
            openWith:'= ', closeWith:' =', placeHolder: 'Nadpis 1. úrovně' },
        { name:'Nadpis 2', className: 'h2', key:'2',
            openWith:'== ', closeWith:' ==', placeHolder: 'Nadpis 2. úrovně' },
        { name:'Nadpis 3', className: 'h3', key:'3',
            openWith:'=== ', closeWith:' ===', placeHolder: 'Nadpis 3. úrovně' },
        { name:'Nadpis 4', className: 'h4', key:'4',
            openWith:'==== ', closeWith:' ====', placeHolder:'Nadpis 4. úrovně' },
        { name:'Nadpis 5', className: 'h5', key:'5',
            openWith:'===== ', closeWith:' =====', placeHolder:'Nadpis 5. úrovně' },
        { separator: '---------------' },
        { name: 'Zvýrazněně', className: 'italic', key: 'I',
            openWith: '""', closeWith: '""' },
        { name: 'Silně', className: 'bold', key: 'B',
            openWith: '"""', closeWith: '"""' },
        { separator: '---------------' },
        { name: 'Seznam s odrážkami', className: 'list-bullet',
            openWith: '\n - ',
            afterInsert: function (markitup) { return lac.afterInsert(markitup); } },
        { name: 'Číslovaný seznam', className: 'list-numeric', 
            openWith: '\n 1. ',
            afterInsert: function (markitup) { return lac.afterInsert(markitup); } },
        { separator: '---------------' },
        { name: 'Odkaz', className: 'url',
            openWith: "([![URL odkazu:!:http://]!] ", closeWith:')', placeHolder: 'Text odkazu' },
        { name: 'Obrázek', className: 'picture',
            openWith: '((obrazek [![URL obrázku::!:http://]!] "', closeWith: '"))', placeHolder: 'Popis obrázku' },
        { separator: '---------------' },
        { name: 'Náhled', call: 'preview', className: 'preview'}
    ]
}

// list auto-creation
lac = {
    append: function (markitup) {
        return this.token ? this.token : '\n';
    },
    afterInsert: function (markitup) {
        this.token = markitup.openWith;
    },
}
