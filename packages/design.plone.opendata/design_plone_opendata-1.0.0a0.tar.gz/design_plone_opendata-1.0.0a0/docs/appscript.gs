//SCRIPT REALIZZATO PER FORMEZPA
//DA FRANCESCO PIERO PAOLICELLI 
//ALL'INTERNO DELLA LINEA 3 "ITALIA LOGIN" DI AGID
//ESEGUI IL DEPLOYMENT --> NUOVO --> COPIARE NELLA RIGA 7 L'URL GENERATO
ID_SPREADSHEET=SpreadsheetApp.getActive().getId();
//Logger.log(ID_SPREADSHEET);
ID_SPREADSHEETAPP='https://script.google.com/macros/s/AKfycbyh2dH1fWI3RLI-Zve5LAZHLSmLcca9-EICrqJq-XOaN3eyCODC3torBrB4JnUqs0rYkw/exec';
    
    I_TITLE=0;
    I_PUBDATE=1;
    I_THEME=2;
    
    function onOpen() {
      
      SpreadsheetApp.getUi()
      .createMenu('AGID')
      .addItem('Genera RDF', 'downloadFile')
      .addToUi();
      doGet();
      // save to drive
      //DriveApp
      //.createFolder('DCATAPIT')
      //.createFile('catalog.rdf',response);
      
    }
    function downloadFile() {
      //var url=ScriptApp.getService().getUrl();
      //Logger.log(url);
      var url=ID_SPREADSHEETAPP;
      var options={'muteHttpExceptions': true};
      var response = UrlFetchApp.fetch(url, options);
      //var response = UrlFetchApp.fetch(url);
      //var text = response.getContentText().replace("_",":");
      var newFile = DriveApp.createFile('catalog.rdf',response);
      debugger;  // Stop to observe if in debugger
      var fileId = newFile.getId();
      var urldownload="https://drive.google.com/uc?export=download&id=" + fileId;
      Logger.log("https://drive.google.com/uc?export=download&id=" + fileId);
      var htmlOutput = HtmlService
      .createHtmlOutput('<a href="'+urldownload+'">Download</a>')
      .setSandboxMode(HtmlService.SandboxMode.IFRAME)
      .setWidth(80)
      .setHeight(60);
      SpreadsheetApp.getUi().showModalDialog(htmlOutput, 'RDF GENERATO');
    }
    
    
    var makeRss = function(){
      var ss = SpreadsheetApp.openById(ID_SPREADSHEET);
      
      var metaSheet = ss.getSheetByName('Catalogo');
      
      
      var linkcatalogo = decodeURIComponent(metaSheet.getRange('F2').getValue().trim());
      
      var rdf = XmlService.createElement('rdf_RDF')
      .setAttribute('xmlns_foaf','http://xmlns.com/foaf/0.1/')
      .setAttribute('xmlns_owl','http://www.w3.org/2002/07/owl#')
      .setAttribute('xmlns_skos','http://www.w3.org/2004/02/skos/core#')
      .setAttribute('xmlns_locn','http://www.w3.org/ns/locn#')
      .setAttribute('xmlns_hydra','http://www.w3.org/ns/hydra/core#')
      .setAttribute('xmlns_rdf','http://www.w3.org/1999/02/22-rdf-syntax-ns#')
      .setAttribute('xmlns_dcat','http://www.w3.org/ns/dcat#')
      .setAttribute('xmlns_dct','http://purl.org/dc/terms/')
      .setAttribute('xmlns_dcatapit','http://dati.gov.it/onto/dcatapit#')
      .setAttribute('xmlns_vcard','http://www.w3.org/2006/vcard/ns#')
      .setAttribute('xmlns_adms','http://www.w3.org/ns/adms#')
      .setAttribute('xmlns_dc','http://purl.org/dc/elements/1.1/')
      .setAttribute('xmlns_gml','http://www.opengis.net/gml/3.2')
      .setAttribute('xmlns_gsp','http://www.opengis.net/ont/geosparql#')
      .setAttribute('xmlns_rdfs','http://www.w3.org/2000/01/rdf-schema#')
      .setAttribute('xmlns_rdf','http://www.w3.org/1999/02/22-rdf-syntax-ns#');
      
      
      var root = XmlService.createElement('vai')
      .addContent(rdf)
      var  formr; 
      var ident = '';
      var title = '';
      var linklp = '';
      var description = '';
      var descrizionedataset ='';
      var language = '';
      var atomlink = '';
      var items = {};
      var ipa ='';
      var foaf='';
      var foaforg='';
      var issued='';
      var modified='';
      var frequence='';
      var puntocontatto='';
      var puntocontattoem='';
      var puntocontattot='';
      var puntocontattow='';
      var puntocontattoname='';
      var ch='';
      var idate='';
      var org='';
      var skos;
      var skoseurovoc;
      var themeuri;
      var eurovoc='';
      var eurovocname='';
      var idr='';
      var urlr;
      var namer;
      var desr;
      var licr;
      var modr;
      var licurir;  
      var dcatlic;
      var dataSheet = ss.getSheetByName('Dataset');
      var dataSheetOrg = ss.getSheetByName('Organizzazione');
      var puntocontattot=dataSheet.getRange(2, 19).getValue();
      var puntocontattoem=dataSheet.getRange(2, 21).getValue();
      var puntocontatto=dataSheet.getRange(2, 17).getValue();
      var puntocontattow=dataSheetOrg.getRange(2, 4).getValue();
      var puntocontattoname=dataSheet.getRange(2, 18).getValue();
      var landingpagediretta = dataSheet.getRange(2, 20).getValue();
      var distribution;
      var distribution1;
      var keyword1='_';
      var keyword2='_';
      var keyword3='_';
      var foafPubC= metaSheet.getRange('C2').getValue();

       var ss = SpreadsheetApp.openById(ID_SPREADSHEET);
       var risorsa = ss.getSheetByName('Risorse');
          

      var createElement = function(element, text){
        return XmlService.createElement(element).setText(text);
      };
      
      
      return {
        setTitle: function(value){ title = value; },
        setLink: function(value){ link = value; },
        setDescription: function(value){ description = value; },
        setLanguage: function(value){ language = value; },
        setAtomlink: function(value){ atomlink = value; },
        setFoam: function(value){ foaf = value; },
        setFoamorg: function(value){ foaforg = value; },
        setIpa: function(value){ ipa = value; },
        setIssued: function(value){ issued = value; },
        setM: function(value){ modified = value; },
        addItem: function(args){
          args.timezone = "GMT"; 
          
          var item = {
            title: args.title,
            linklp: linkcatalogo,
            landingpagediretta: args.landingpagediretta,
            description: args.description,
            //    pubDate: args.pubDate,
            pubDate: args.pubDate,
            guid: args.guid,
            ipa: args.ipa,
            foaf: args.foaf,
            atomlink: args.atomlink,
            modified: args.modified,
            ident: args.ident,
            frequence: args.frequence,
            themeuri: args.themeuri,
            descrizionedataset: args.descrizionedataset,
            idate: args.idate,
            idr: args.idr,
            urlr: args.urlr,
            namer: args.namer,
            desr: args.desr,
            licr: args.licr,
            formr:  args.formr,
            modr: args.modr,
            licurir: args.licurir,
            eurovoc: args.eurovoc,
            eurovocname: args.eurovocname,
            keyword1: args.keyword1,
            keyword2: args.keyword2,
            keyword3: args.keyword3,
      
          }
          
          items[item.ident] = item;
        },
        
        toString: function(){
          
          var rdf1=XmlService.createElement("rdf_type")
          .setAttribute('rdf_resource', 'http://www.w3.org/ns/dcat#Catalog')
          
          ch= XmlService.createElement('dcatapit_Catalog')
          .setAttribute('rdf_about', linkcatalogo)
          .addContent(rdf1);
          
          ch.addContent(createElement('dct_title', title));
          
          var skos=XmlService.createElement('skos_ConceptScheme')
          .setAttribute('rdf_about','http://publications.europa.eu/resource/authority/data-theme')
          .addContent(createElement('dct_title','Data Theme Vocabulary'))
          
          var th= XmlService.createElement('dcat_themeTaxonomy')
          .addContent(skos);
          
          var pubr= XmlService.createElement('rdf_type')
          .setAttribute('rdf_resource','http://xmlns.com/foaf/0.1/Organization')
          var pubr1= XmlService.createElement('rdf_type')
          .setAttribute('rdf_resource','http://xmlns.com/foaf/0.1/Agent')
          var chp = XmlService
          .createElement('dcatapit_Agent')
          .setAttribute('rdf_about',ipa)
          .addContent(pubr)
          .addContent(pubr1)
          .addContent(createElement('dct_identifier',ipa))
          .addContent(createElement('foaf_name',foafPubC))
          // fix editore catalogo
          
          // var pub= XmlService.createElement('rdf_resource')
          
          var pubrdf =XmlService.createElement('dct_publisher')
          
          .addContent(chp);
          ch.addContent(pubrdf)
          
          //   ch.addContent(createElement('dct_publisher','')).addContent(chp);             
          ch.addContent(createElement('dct_description', description));
          ch.addContent(createElement('dct_language', language));
          ch.addContent(createElement('foaf_homepage','')
                        .setAttribute('rdf_resource',linkcatalogo+"#")
                       );
          
          
          ch.addContent(th);
          
          var datenorm=Utilities.formatDate(issued, 'GMT+1', "yyyy-MM-dd");
          var datenormm=Utilities.formatDate(modified, 'GMT+1', "yyyy-MM-dd");
          
          
          ch.addContent(createElement('dct_modified',datenormm.toString())
                        .setAttribute('rdf_datatype','http://www.w3.org/2001/XMLSchema#date')
                       );
          
          ch.addContent(createElement('dct_issued',datenorm.toString())
                        .setAttribute('rdf_datatype','http://www.w3.org/2001/XMLSchema#date')
                       );
          
          ch.addContent(createElement('dct_license','')
                        .setAttribute('rdf_resource','https://creativecommons.org/licenses/by/4.0/')
                       );

          var rdftype=XmlService
          .createElement('rdf_type')
          .setAttribute('rdf_resource','http://www.w3.org/2006/vcard/ns#Voice') 
          var chpcem = XmlService
          .createElement('vcard_hasEmail')
          .setAttribute('rdf_resource',puntocontattoem) 
          
          var chpct = XmlService
          .createElement('vcard_hasTelephone')
          .setAttribute('rdf_parseType','TelephoneType')   
          .addContent(createElement('vcard_value', puntocontattot))
          .addContent(rdftype)
          
          var chpcw = XmlService
          .createElement('vcard_hasURL')
          .setAttribute('rdf_resource',puntocontattow)                       
          
          var orgtyp = XmlService
          .createElement('rdf_type')                     
          .setAttribute('rdf_resource','vcard_Organization')                       
         // .setAttribute('rdf_resource','http://www.w3.org/2006/vcard/ns#Organization')                       
         var orgtyp1 = XmlService
          .createElement('rdf_type')
          .setAttribute('rdf_resource','vcard_Kind')
          
           var orgtyp2 = XmlService
          .createElement('rdf_type')                     
          .setAttribute('rdf_resource','http://xmlns.com/foaf/0.1/Organization')  
           var orgtyp3 = XmlService
          .createElement('rdf_type')                     
          .setAttribute('rdf_resource','http://www.w3.org/2006/vcard/ns#Kind')  
           var orgtyp4 = XmlService
          .createElement('rdf_type')                     
          .setAttribute('rdf_resource','http://www.w3.org/2006/vcard/ns#Organization')  
            
   
          org =XmlService
          .createElement('dcatapit_Organization')
          .setAttribute('rdf_about',puntocontattow)
          .addContent(orgtyp)
          .addContent(orgtyp2)
          .addContent(orgtyp3)
          .addContent(orgtyp4)
          .addContent(orgtyp1)
          .addContent(createElement('vcard_fn', puntocontattoname))
          .addContent(chpcem)
          .addContent(createElement('vcard_hasTelephone', puntocontattot))
          .addContent(chpcw)
          
        
          for (var i in items) 
          {
         
           var urldataset=items[i].linklp+'/'+items[i].ident;
           urldataset = urldataset.replaceAll(ipa+"|",""); 
     
            ch.addContent(createElement('dcat_dataset','')
                          .setAttribute('rdf_resource',urldataset)
                         );   
           
          }
          
          ch.addContent(createElement('dcatapit2Catalog','piersoft'));
          // </dcatapit2Catalog>
          
         
          
          for (var i in items) {
            
            var rig=  XmlService.createElement('rdf_type')
            .setAttribute('rdf_resource','http://xmlns.com/foaf/0.1/Agent')
            var chprig = XmlService
            .createElement('dcatapit_Agent')
            .setAttribute('rdf_about',ipa)
            .addContent(rig)
            .addContent(createElement('dct_identifier',ipa))
            .addContent(createElement('foaf_name',foaforg))
            
            var right =XmlService.createElement('dct_rightsHolder')
            .addContent(chprig); 
            
            var chf = XmlService
            .createElement('dct_accrualPeriodicity')
            .setAttribute('rdf_resource',items[i].frequence)
            var chpc = XmlService
            .createElement('dcat_contactPoint')
            .setAttribute('rdf_resource',puntocontattow)                       
            
            var rdftyp=XmlService
            .createElement('rdf_type')
            .setAttribute('rdf_resource','http://www.w3.org/ns/dcat#Dataset') 
            var themeuri= XmlService
            .createElement('dcat_theme')
            .setAttribute('rdf_resource',items[i].themeuri);    
            //Logger.log(items[i].themeuri);                   
            
            var pubr= XmlService.createElement('rdf_type')
            .setAttribute('rdf_resource','http://xmlns.com/foaf/0.1/Organization')
            var pubr1= XmlService.createElement('rdf_type')
            .setAttribute('rdf_resource','http://xmlns.com/foaf/0.1/Agent')
            
            var chp = XmlService
            .createElement('dcatapit_Agent')
            .setAttribute('rdf_nodeID','Nd117aa7f2e7b47fb9481d4a8aca59c7d')
            .addContent(pubr)
            .addContent(pubr1)
            .addContent(createElement('dct_identifier',ipa))
            .addContent(createElement('foaf_name',foaforg))
            
            var pubrdf =XmlService.createElement('dct_publisher')
            .addContent(chp);
            
            var datenormm=Utilities.formatDate(items[i].pubDate, 'GMT+1', "yyyy-MM-dd");
            var datenormi=Utilities.formatDate(items[i].idate, 'GMT+1', "yyyy-MM-dd");           
            
            var risorsa1 = ss.getSheetByName('Risorse');
            
            var rigarf;  
            var rigarf1;     
            var filtro=items[i].ident;
            
            var distribution=XmlService.createElement('dcat_distribution');
            var accu=XmlService.createElement('dcat_accessURL');
            var licris=XmlService.createElement('dct_license');
            
            var dcatapitLicenseDocument =  XmlService.createElement('dcatapit_LicenseDocument')
                                           .addContent(createElement('rdf_type','').setAttribute('rdf_resource','dct_LicenseDocument'))
                                           .addContent(createElement('dct_type','').setAttribute('rdf_resource','http://purl.org/adms/licencetype/Attribution'));
                                           
                                          
            var licensed=XmlService.createElement('dct_license')

            var eur=XmlService
            .createElement('dct_subject')
           // .setAttribute('rdf_resource','http://eurovoc.europa.eu/'+items[i].eurovoc)
            
            var skoslab=createElement('skos_prefLabel',items[i].guid);
            
            
            skos=  XmlService.createElement('skos_Concept')
            .setAttribute('rdf_about',items[i].themeuri)
            .addContent(skoslab)
            
            ch.addContent(skos);  
            
            
            var skoseu=createElement('skos_prefLabel',items[i].eurovocname)
                         .setAttribute('xml_lang','it')

            skoseurotype= XmlService.createElement('rdf_type')
            .setAttribute('rdf_resource','http://dati.gov.it/onto/dcatapit#subTheme')
        
            
            skoseurovoc=  XmlService.createElement('skos_Concept')
            .setAttribute('rdf_about','http://eurovoc.europa.eu/'+items[i].eurovoc)
            

            skoseurovoc.addContent(skoseurotype);
            skoseurovoc.addContent(skoseu);
            eur.addContent(skoseurovoc);  


            var accrig=XmlService
            .createElement('dct_accessRights')
            .setAttribute('rdf_resource','http://publications.europa.eu/resource/authority/access-right/PUBLIC');
                                     
            var cpoint =XmlService
          .createElement('dcat_contactPoint')
          .setAttribute('rdf_resource',puntocontattow)
           //Logger.log(distribution)  
            var keywords1;
            var keywords2;
            var keywords3;
            if (items[i].keyword1.length>1) keywords1=createElement('dcat_keyword',items[i].keyword1);
            if (items[i].keyword2.length>1) keywords2=createElement('dcat_keyword',items[i].keyword2);
            if (items[i].keyword3.length>1) keywords3=createElement('dcat_keyword',items[i].keyword3);
           var urldataset=items[i].linklp+'/'+items[i].ident;
           urldataset = urldataset.replaceAll(ipa+"|",""); 
           var landingpage=XmlService
          .createElement('dcat_landingPage')
          .setAttribute('rdf_resource',items[i].landingpagediretta+'/')

           Logger.log('key in dataset: '+ keyword1) ;
      
            var dataset =  XmlService
            .createElement('dcatapit_Dataset')
            .setAttribute('rdf_about',urldataset)
            .addContent(rdftyp)
            .addContent(accrig)
            .addContent(themeuri)
            .addContent(licensed)
            .addContent(createElement('dct_title', items[i].title))
            .addContent(landingpage)
            .addContent(createElement('dct_description', items[i].descrizionedataset))                                          
            .addContent(createElement('dct_identifier', items[i].ident))
            .addContent(chf)
            .addContent(chpc)
            .addContent(right)
            .addContent(pubrdf)
            .addContent(eur)
            .addContent(createElement('dct_language','').setAttribute('rdf_resource','http://publications.europa.eu/resource/authority/language/ITA'))
             .addContent(createElement('dct_license','')
                        .setAttribute('rdf_resource','https://creativecommons.org/licenses/by/4.0/'))
            .addContent(createElement('dct_modified',datenormm)
                        .setAttribute('rdf_datatype','http://www.w3.org/2001/XMLSchema#date'))
            .addContent(createElement('dct_issued',datenormi)
                        .setAttribute('rdf_datatype','http://www.w3.org/2001/XMLSchema#date'))
            .addContent(cpoint);     
            if (items[i].keyword1.length>1) dataset.addContent(keywords1);
            if (items[i].keyword2.length>1) dataset.addContent(keywords2);
            if (items[i].keyword3.length>1) dataset.addContent(keywords3);
            Logger.log('numero di risorse: '+ risorsa.getMaxRows()) ;
            for (var ii=2; ii <= risorsa.getMaxRows(); ii++) {
              var rigar=risorsa.getRange(ii,1,1,7).getValues();
              
              
              if (filtro==risorsa.getRange(ii, 1).getValue()){
                rigarf++;
                
                idr=rigar[0][0];
                urlr=rigar[0][1];
                urlr = urlr.replaceAll('_','%5F');
                namer=rigar[0][2];
                namer = namer.replaceAll('_','-');
                desr=rigar[0][3];
                licr=rigar[0][4];
                //  formr=rigar[0][5];
                formr=risorsa.getRange(ii, 6).getValue();
                Logger.log('url risorsa: '+urlr);
                
                modr=rigar[0][6];
                licurir=risorsa.getRange(ii, 8).getValue();
                //Logger.log(licurir);
            //    dcatapitLicenseDocument.setAttribute('rdf:about',licurir);
             //   dcatapitLicenseDocument.addContent(createElement('foaf_name',licr));
              //  licris.addContent(licr)
               
                accu.setAttribute('rdf_resource',urlr);
              var urldataset=items[i].linklp+'/'+items[i].ident;
           urldataset = urldataset.replaceAll(ipa+"|",""); 
     
                //Logger.log(distribution);
               dataset.addContent(createElement('dcat_distribution','').setAttribute('rdf_resource',urldataset+'/'+formr.toLowerCase()+ii));
              }
            
                        
            }
      
           
            ch.addContent(dataset);

          }
          for (var i in items) 
          {
            var filtro=items[i].ident;
     
            
          //<dct:description >File in formato csv</dct:description> 
       
           for (var ii=2; ii <= risorsa.getMaxRows(); ii++) {
              var rigar=risorsa.getRange(ii,1,1,7).getValues();
              
              
              if (filtro==rigar[0][0]){
                rigarf1++;
                
                idr=rigar[0][0];
                urlr=rigar[0][1];
                namer=rigar[0][2];
                namer = namer.replaceAll('_','-');
                descriz=rigar[0][3];
                licr=rigar[0][4];
                //  formr=rigar[0][5];
                formr=risorsa.getRange(ii, 6).getValue();
                urlr = urlr.replaceAll('_','%5F');
                modr=rigar[0][6];
                licurir=risorsa.getRange(ii, 8).getValue();
        
         var accu=XmlService.createElement('dcat_accessURL');
            
         var rdfdct1=XmlService.createElement('rdf_type')
            .setAttribute('rdf_resource','dct:LicenseDocument')
            var dct1=XmlService.createElement('dct_type')
            .setAttribute('rdf_resource','http://purl.org/adms/licencetype/Attribution')
            
            var dcatlic=XmlService.createElement('dcatapit_LicenseDocument')
            .setAttribute('rdf_about','https://creativecommons.org/licenses/by/4.0/')
            .addContent(rdfdct1)
            .addContent(dct1)
            
            var licris=XmlService.createElement('dct_license')
            var risform=XmlService.createElement('dct_format')
            var accrigdist=XmlService
            .createElement('dct_rights')
            .setAttribute('rdf_resource','http://publications.europa.eu/resource/authority/access-right/PUBLIC');

            
               // var foaf=XmlService.createElement('foaf_name','a');
                risform.setAttribute('rdf_resource',formr);
                accu.setAttribute('rdf_resource',urlr);
                 
                dcatlic.setAttribute('rdf_about',licurir)
                //licris.setAttribute('rdf_resource','http://www.w3.org/ns/dcat#Distribution') 
                dcatlic.addContent(createElement('foaf_name',licr));
                licris.addContent(dcatlic)
                //Logger.log(dcatlic);
                 var rdftypr=XmlService
            .createElement('rdf_type')
            .setAttribute('rdf_resource','http://www.w3.org/ns/dcat#Distribution') 
          
            var urldataset=items[i].linklp+'/'+items[i].ident;
            urldataset = urldataset.replaceAll(ipa+"|",""); 
     
            var distribution1 =XmlService.createElement('dcatapit_Distribution')
            .setAttribute('rdf_about',urldataset+'/'+formr.toLowerCase()+ii)
            .addContent(accu)
            .addContent(licris)
            .addContent(risform)
            .addContent(accrigdist)
            .addContent(createElement('dct_description',descriz))
            .addContent(createElement('dct_title',namer))
            .addContent(rdftypr);
            
            
               ch.addContent(distribution1);
              }
            }
            
           
            
          }
          /*
          for (var i in items) 
          {
            var skoslab=createElement('skos_prefLabel',items[i].guid);
            
            
            skos=  XmlService.createElement('skos_Concept')
            .setAttribute('rdf_about',items[i].themeuri)
            .addContent(skoslab)
            
            ch.addContent(skos);  
            
            
            var skoseu=createElement('skos_prefLabel',items[i].eurovocname)
                         .setAttribute('xml_lang','it')

            skoseurotype= XmlService.createElement('rdf_type')
            .setAttribute('rdf_resource','http://dati.gov.it/onto/dcatapit#subTheme')
        
            
            skoseurovoc=  XmlService.createElement('skos_Concept')
            .setAttribute('rdf_about','http://eurovoc.europa.eu/'+items[i].eurovoc)
            .addContent(skoseu)

            skoseurovoc.addContent(skoseurotype);
            ch.addContent(skoseurovoc);   
            
          }
          
          */
          var document = XmlService.createDocument(root);
          
          var xml = XmlService.getPrettyFormat().format(document)
          xml += XmlService.getPrettyFormat().format(ch)
          // xml += '\n'+XmlService.getPrettyFormat().format(dataset)
          // xml += '\n'+XmlService.getPrettyFormat().format(skos)
          xml += XmlService.getPrettyFormat().format(org)
          
          
          var result = xml.replace('_', ':');
          result = result.replace('</vai>','');
          result = result.replace('<vai>','');  
          //result = result.replace('$%$','$5F');  
          
          return result;
        }
        
      };
    };
    
    
    /*
    function onOpen() {
    SpreadsheetApp.getUi() // Or DocumentApp or SlidesApp or FormApp.
    .createMenu('Custom Menu')
    .addItem('Show alert', 'open')
    .addToUi();
    }
    */
    function doGet() { 
      var ss = SpreadsheetApp.openById(ID_SPREADSHEET);
      
      var metaSheet = ss.getSheetByName('Catalogo');
      
      var RSSFeedTitle = metaSheet.getRange('A2').getValue();
      var RSSFeedURI = decodeURIComponent(metaSheet.getRange('F2').getValue().trim());
      var RSSFeedDesc = metaSheet.getRange('B2').getValue();
      var RSSFeedIpa = metaSheet.getRange('D2').getValue();
      var RSSFeedD = metaSheet.getRange('E2').getValue();
      var RSSFeedPubEdit = metaSheet.getRange('C2').getValue();
      var RSSFeedM = metaSheet.getRange('G2').getValue();
      
      var dataSheet = ss.getSheetByName('Dataset');
      var risorsa = ss.getSheetByName('Risorse');
      var org = ss.getSheetByName('Organizzazione');
      var RSSFeedPublisher = org.getRange('B2').getValue();
      //Logger.log('org:'+RSSFeedPublisher);
      var rss=makeRss();
      
      
      rss.setTitle(RSSFeedTitle);
      rss.setLink(RSSFeedPublisher);
      rss.setFoamorg(RSSFeedPublisher);
      rss.setDescription(RSSFeedDesc);
      rss.setLanguage('it');
      rss.setAtomlink(RSSFeedURI);
      rss.setIpa(RSSFeedIpa);
      rss.setFoam(RSSFeedTitle);
      rss.setIssued(RSSFeedD);
      rss.setM(RSSFeedM);

      // Logger.log('numero righe:'+dataSheet.getMaxRows()) 
      
      for (var i=2; i <= dataSheet.getMaxRows(); i++) {
        
        var riga=dataSheet.getRange(i,1,1,28).getValues();
        
        var ident=riga[0][1];
        
        if (ident.length==0) {
          break;
        }else{
          
          var linklp=riga[0][19]+riga[0][1];
          var landingpagediretta= riga[0][19];
//Logger.log("Landingpage: "+landingpagediretta)
          var myguid=riga[0][I_THEME];
          var titolo=riga[0][I_TITLE];
          var descrizione=riga[0][3];
          var pDate=riga[0][8]; 
          var iDate=riga[0][7]; 
          var foafdat=riga[0][6]; 
          var ipadat=riga[0][5]; 
          var ident=riga[0][1];
          var frequence=riga[0][15];
          var eurovoc=riga[0][22];
          var themeuri=riga[0][14];
          var eurovocname=riga[0][23];
          var keyword1=riga[0][24];
          var keyword2=riga[0][25];
          var keyword3=riga[0][26];
          //if (keyword1.length<1) keyword1='N/A';
          //if (keyword2.length<1) keyword2='N/A';
          //if (keyword3.length<1) keyword3='N/A';
          Logger.log(themeuri);
        }
        var puntocontattot=dataSheet.getRange(2, 19).getValue();
        var puntocontattoem=dataSheet.getRange(2, 21).getValue();
        var puntocontatto=dataSheet.getRange(2, 17).getValue();
        var puntocontattow=dataSheet.getRange(2, 20).getValue();
        var puntocontattoname=dataSheet.getRange(2, 18).getValue();

        /*
        for (var ii=2; ii < risorsa.getMaxRows(); ii++) {
        var rigar=risorsa.getRange(ii,1,1,21).getValues();
        
        
        if (ident=rigar[0][1]){
        
        var idr=rigar[0][0];
        var urlr=rigar[0][1];
        var namer=rigar[0][2];
        var desr=rigar[0][3];
        var licr=rigar[0][4];
        var formr=rigar[0][5];
        var modr=rigar[0][6];
        var licurir=rigar[0][7];
        //Logger.log(rigar);
        if (idr.length==0) {
        break;
        }
        }
        }
        */
        var pDateFix=pDate;
        
        if (pDateFix.length > 0) {
          var pubDateDate = new Date(pDateFix);
        } else {
          var pubDateDate = new Date();
        }
        
        rss.addItem({title: titolo,
                     guid:myguid,
                     linklp: linklp,
                     landingpagediretta: landingpagediretta,
                     description: titolo,
                     pubDate: pDate,
                     idate: iDate,
                     ipa: ipadat,
                     foaforg: RSSFeedPublisher,
                     foaf: foafdat,
                     foafPubC: RSSFeedPubEdit,
                     ident: ident,
                     frequence: frequence,
                     puntocontatto: puntocontatto,
                     puntocontattoem: puntocontattoem,
                     puntocontattot: puntocontattot,
                     puntocontattow: puntocontattow,
                     puntocontattoname: puntocontattoname,
                     themeuri: themeuri,
                     descrizionedataset: descrizione,
                     eurovoc: eurovoc,
                     eurovocname: eurovocname,
                     keyword1: keyword1,
                     keyword2: keyword2,
                     keyword3: keyword3,
                     
                     /*       idr: idr,
                     urlr: urlr,
                     namer: namer,
                     desr: desr,
                     licr: licr,
                     formr:  formr,
                     modr: modr,
                     licurir: licurir*/
                    });
      }
      
      var rssStr=rss.toString().replaceAll("_",":");
      //var rssStr=rss.toString().replaceAll("ct_","ct:");
      rssStr = rssStr.replaceAll('it_','it:');
      rssStr = rssStr.replaceAll('rdf_','rdf:');

      rssStr = rssStr.replaceAll('PIERSOFT','_');

      var resultn = rssStr.replace('</vai>','');
      Logger.log('ipadat -> '+RSSFeedIpa);
      ipanew=RSSFeedIpa.replaceAll('___','_');
      var idold=ipanew+"_"+ident;
      var idnew=ipanew+":"+ident;
      Logger.log('idold -> '+idold);
      Logger.log('idnew-> '+idnew);
      resultn = resultn.replace('<vai>','');
      resultn = resultn.replace('</dcatapit:Organization>','</dcatapit:Organization>\n</rdf:RDF>');
      resultn = resultn.replace('xmlns_','xmlns:');
      resultn = resultn.replace('UTF-8','utf-8');   
      resultn = resultn.replace('#" />','#" >');   
      resultn = resultn.replaceAll(' />','/>'); 
      resultn = resultn.replace('</dcatapit:Catalog>','');
      resultn = resultn.replaceAll(':::','_') // patch per identifier      
      resultn = resultn.replaceAll('<dcatapit2Catalog>piersoft','');
      resultn = resultn.replaceAll('dcatapit2Catalog','dcatapit:Catalog');
      resultn = resultn.replaceAll(' >','>'); 
      resultn = resultn.replaceAll('|','_'); 
      resultn = resultn.replaceAll('c:','c_'); 
      resultn = resultn.replaceAll('r:','r_'); 
      resultn = resultn.replaceAll('m:','m_'); 
      resultn = resultn.replaceAll('A21:CCBY40','A21_CCBY40'); 
      resultn = resultn.replaceAll('A310:ODBL','A310_ODBL'); 
      resultn = resultn.replaceAll('documento:pubblico','documento_pubblico');
      resultn = resultn.replaceAll('A11:CCO10','A11_CCO10');
      resultn = resultn.replaceAll('licences/A29:IODL20','licences/A29_IODL20');
      resultn = resultn.replaceAll('A31:CCBYSA40','A31_CCBYSA40');
      resultn = resultn.replaceAll('p:av','p_av');
      resultn = resultn.replaceAll('A1:PublicDomain','A1_PublicDomain');
      resultn = resultn.replaceAll('comune-di-bugliano/"','comune-di-bugliano"')
      resultn = resultn.replaceAll('comune.bugliano.it//comune-di-bugliano','comune.bugliano.it/comune-di-bugliano')
      resultn = resultn.replaceAll('ANNUAL:2','ANNUAL_2');
      resultn = resultn.replaceAll('ANNUAL:3','ANNUAL_3');
      resultn = resultn.replaceAll('DAILY:2','DAILY_2');
      resultn = resultn.replaceAll('MONTHLY:2','MONTHLY_2');
      resultn = resultn.replaceAll('MONTHLY:3','MONTHLY_3');
      resultn = resultn.replaceAll('WEEKLY:2','WEEKLY_2');
      resultn = resultn.replaceAll('WEEKLY:3','WEEKLY_3');
      resultn = resultn.replaceAll(idold,idnew); 
      Logger.log('ipad+ident -> '+ipanew+":"+ident) 
      var A1String = resultn.toString().replaceAll(" />", "/>");
   
     // Logger.log(rssStr)
      Logger.log(dataSheet.getMaxRows());
      Logger.log(A1String) 
      
      return ContentService.createTextOutput(A1String).setMimeType(ContentService.MimeType.XML);
    }
    
 function getScriptURL() {
  Logger.log(ScriptApp.getService().getUrl());
  return ScriptApp.getService().getUrl();
}
function randomStr(m) {
    var m = m || 31; s = '', r = 'Nd117aa7f2e7b47fb9481d4a8aca59c7d';
    for (var i=0; i < m; i++) { s += r.charAt(Math.floor(Math.random()*r.length)); }
    return s;
};