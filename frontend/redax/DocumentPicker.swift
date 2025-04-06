//
//  DocumentPicker.swift
//  redax
//
//  Created by Mariana Isabel Gonzalez Reyes on 4/5/25.
//

import SwiftUI
import UniformTypeIdentifiers // Used to specify document types, e.g., UTType.pdf

// `DocumentPicker` - View that wraps a UIKit document picker.
struct DocumentPicker: UIViewControllerRepresentable {
    
    // Closure that will be called when the user picks one or more documents
    var onDocumentsPicked: ([URL]) -> Void

    // Creates the coordinator that acts as a delegate between SwiftUI and UIKit
    func makeCoordinator() -> Coordinator {
        Coordinator(onDocumentsPicked: onDocumentsPicked)
    }

    // Creates and configures the UIDocumentPickerViewController
    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        // Set up the picker to open PDF files and make a copy of them
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [UTType.pdf], asCopy: true)
        picker.allowsMultipleSelection = false // Only one file can be selected
        picker.delegate = context.coordinator   // Assign the coordinator as the delegate
        return picker
    }

    // Required method for UIViewControllerRepresentable, but not needed here
    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}

    // Internal class used as the delegate for UIDocumentPickerViewController
    class Coordinator: NSObject, UIDocumentPickerDelegate {
        
        // Store the callback to send selected documents back to SwiftUI
        let onDocumentsPicked: ([URL]) -> Void

        // Initialize the coordinator with the callback
        init(onDocumentsPicked: @escaping ([URL]) -> Void) {
            self.onDocumentsPicked = onDocumentsPicked
        }

        // Called when the user selects one or more documents
        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            onDocumentsPicked(urls) // Pass selected document URLs back via the callback
        }
    }
}



