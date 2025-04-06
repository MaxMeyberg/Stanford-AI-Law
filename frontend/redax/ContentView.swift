//
//  ContentView.swift
//  redax
//
//  Created by Mariana Isabel Gonzalez Reyes on 4/5/25.
//

//
//  ContentView.swift
//  redax
//
//  Created by Mariana Isabel Gonzalez Reyes on 4/5/25.
//

import SwiftUI
import UniformTypeIdentifiers
import PDFKit


struct ContentView: View {
    
    
    
    @State private var showPicker = false
    @State private var selectedPDF: URL?
    
    //FOR TEXTFIELD
    @State private var context: String = ""

    var body: some View {
        VStack {
            //Spacer(minLength: 10)

            VStack {
                HStack {
                    
                    //TITLE
                    Text("REDAX")
                        .fontWeight(.bold)
                        .fontDesign(.rounded)
                        .font(.largeTitle)
                    
//                        .font(.system(size: 28, weight: .semibold))

                    Image(systemName: "highlighter")
                        .imageScale(.large)
                        .foregroundStyle(.tint)
                }
        

                Text("A faster way to redax documents")
                    .font(.title2)
                    .fontDesign(.rounded)

                
            }
            HStack {
                
                Text("Advanced AI-powered software solution that automates the redaction of sensitive information in documents, ensuring full compliance with the Freedom of Information Act (FOIA) and related privacy regulations. Leveraging cutting-edge Natural Language Processing (NLP) and Machine Learning (ML), the software identifies, classifies, and redacts sensitive data with precision, including Personally Identifiable Information (PII), classified content, and protected legal or investigative materials.")
                
                //Spacer(minLength: 10)
                
            }.padding(20)

            if let pdf = selectedPDF {
                PDFKitView(url: pdf)
                    .frame(maxHeight: 400)
                    .padding()
            } else {
                
                
                //UPLOAD BUTTON SHOULD BE HERE
                
                VStack {
                    
                    Spacer()
                    
                    
                    Button(action: {
                        showPicker = true
                    }) {
                        Image(systemName: "square.and.arrow.up.circle")
                            .imageScale(.large)
                            .foregroundStyle(.tint)
                            .font(.system(size: 250))
                    }
                    .padding(20)

                    if let pdf = selectedPDF {
                        Text("Selected: \(pdf.lastPathComponent)")
                            .font(.caption)
                            .foregroundColor(.gray)
                            .padding()
                    }
                }
                .sheet(isPresented: $showPicker) {
                    DocumentPicker { urls in
                        selectedPDF = urls.first
                        showPicker = false
                    }
                }
                
                Spacer(minLength: 250)
                
                //.padding(150)

            }
        
        }

            
            Divider()
            Spacer()
            
            
            
            //CONTEXT TITLE
            
            
            Text("Input the context of the document: ")
                .font(.title3)
                .fontDesign(.rounded)
                .padding(20)
        
            
            
            //TEXT FIELD FOR CONTEXT
            HStack {
                TextField("Message...", text: self.$context)
                    .font(.system(size: 20)) // make
                    .padding(.vertical, 20)
            }
            .padding()
            .background(Color.indigo.opacity(0.05))
            .frame(height: 80)
            .cornerRadius(10)
            .fontDesign(.rounded)
            .frame(height: 50)
            
            
            Divider()
            Spacer(minLength: 20)
            
        
        Button(
          "Upload PDF File and Document Context",
          action: {
            // Action to perform
          }
        )
        //.frame(width: 100, height: 100)
        .font(.title3)
        .padding(30)
        .foregroundColor(.white)
        .background(.blue)
        .cornerRadius(10)
        
        
        Spacer(minLength: 80)
        
        
            

    }

        
}
  

// MARK: - PDF Viewer with PDFKit

struct PDFKitView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> PDFView {
        let pdfView = PDFView()
        pdfView.autoScales = true
        pdfView.displayMode = .singlePageContinuous
        pdfView.displayDirection = .vertical
        pdfView.document = PDFDocument(url: url)
        return pdfView
    }

    func updateUIView(_ uiView: PDFView, context: Context) {}
}


#Preview {
    ContentView()
}



/*
 
 NOTES:
 
//context of the case

//ATTORNEY CLIENT PRIVILEDGE
//WORK PRODUCT

//GREEN I FSURE
//YELLOW
//LEARNING WHULE YOU ARE DOING IT
//YES OR NO BUTTON
 
 Jurisdiction rules that we want to build
*/
