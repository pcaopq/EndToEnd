//
//  main.cpp
//  processxml
//
//  Created by Panfeng Cao on 16/5/25.
//  Copyright © 2016年 Panfeng Cao. All rights reserved.
//    doc.LoadFile( "0003.xml" );
//    static const char* xml = "<element/>";
//    doc.Parse(xml);
//    static const char* xml1 = "<?xml version=\"1.0\"?>"
//    "<!DOCTYPE PLAY SYSTEM \"play.dtd\">"
//    "<PLAY>"
//    "<TITLE>A Midsummer Night's Dream</TITLE>"
//    "</PLAY>";
//    doc.Parse(xml1);
//    XMLElement* titleElement = doc.FirstChildElement( "PLAY" )->FirstChildElement( "TITLE" );
//    const char* title = titleElement->GetText();
//    printf( "Name of play (1): %s\n", title );
//    XMLText* textNode = titleElement->FirstChild()->ToText();
//    title = textNode->Value();
//    printf( "Name of play (2): %s\n", title );
//    static const char* xml =
//    "<information>"
//    "   <attributeApproach v='2' />"
//    "   <textApproach>"
//    "       <v>2</v>"
//    "   </textApproach>"
//    "</information>";
//    doc.Parse(xml);
//    int v0;
//    int v1;
//    XMLElement* attributeApproachElement = doc.FirstChildElement()->FirstChildElement( "attributeApproach" );
//    attributeApproachElement->QueryIntAttribute( "v", &v0 );
//
//    XMLElement* textApproachElement = doc.FirstChildElement()->FirstChildElement( "textApproach" );
//    textApproachElement->FirstChildElement( "v" )->QueryIntText( &v1 );
//    cout<<v0<<endl;
//    cout<<v1<<endl;

#include <iostream>
#include <vector>
#include "tinyxml2.cpp"
using namespace tinyxml2;
using namespace std;
int main(int argc, const char * argv[]) {
    clock_t begin = clock();
    XMLDocument doc;
    XMLError eResult = doc.LoadFile("0003.xml");
//    doc.Parse("0003.xml");
//     XMLElement* pElement = doc.FirstChildElement("alto")->FirstChildElement("Layout")->FirstChildElement("Page")->FirstChildElement("PrintSpace")->FirstChildElement("TextBlock");
    // int hpos[100];
    // tmp->QueryIntAttribute("HPOS", hpos);
    XMLNode * pRoot = doc.FirstChildElement("alto");
//    if(pRoot == NULL)
//    	return XML_ERROR_FILE_READ_ERROR;
    XMLElement * pElement = pRoot->FirstChildElement("Layout")->FirstChildElement("Page")->FirstChildElement("PrintSpace")->FirstChildElement("TextBlock");
//	if (pElement == nullptr)
//		return XML_ERROR_PARSING_ELEMENT;
//	XMLElement * pListElement = pElement->FirstChildElement("HPOS");
	vector<int> vecList;
	while (pElement != nullptr)
	{
		int iOutListValue;
		eResult = pElement->QueryIntAttribute("HPOS", &iOutListValue);
//		XMLCheckResult(eResult);
		vecList.push_back(iOutListValue);
		pElement = pElement->NextSiblingElement("TextBlock");
	}
    clock_t end = clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    cout<<elapsed_secs<<endl;
    for(auto i:vecList)
        cout<<i<<" ";
    cout<<endl;
    cout<<vecList.size()<<endl;
    return 0;
}
















