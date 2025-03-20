# Tikos Reasoning Platform

Tikos Reasoning Platform harnesses the power of empirically established 2nd-generation AI and statistical toolsets to offer its users advanced 3rd-generation AI capabilities.

Copyright 2024 (C) Tikos Technologies Limited

## How to access the platform

To get Alpha API keys, please register your request via https://tikos.tech/

## Licence

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Release Notes

1. v 0.0.7, added 

   i. GetGraphStructure: Automatically extract graph Vertices and Edges that can be further refined by the user

   ii. GenerateGraph: Provide Tikos Reasoning Platform the refined graph Vertices and Edges to build the standard knowledge graph

   iii. GetGraph: Get the whole graph for an extraction request

   iv. GetGraphRelationships: Get relationships between two Vertexes

2. v 0.0.8, added

   i. GetGraphRetrieval: Retrieve query response along with the Graph relationships for the requested retrieve query

3. v 0.0.9, added

   i. GetGraphRetrievalWithDS: Retrieve query response along with the Graph relationships for the requested retrieve query with Graph Node data sets as JSON

4. v 0.1.0, added

   i. Licence conditions

5. v 0.1.1

   i. Added, ProcessExtractFile: Be able to extract data from a specific file and support JSON based extraction using jq based schemas

   ii. Modified, ProcessExtract: Support JSON based extraction using jq based schemas

6. v0.1.1

   i. Added, BuildSC: Generate the SequentialCollection knowledge structure for the associated graph Vertices from structured data sets

   ii. Added, GetSimilarCase: Providing a Problem Space (PS) case, the Sequential collection will contact a basic binary (BIN, default) search or advanced binary (BINADV) search and return the most similar existing case. This does not perform any case adaptation

7. v0.1.4

   i. Added, GetGraphStructurePerDoc: Accept a file names and generate NER JSON of the (submitted) file

   ii. Added, GenerateGraphPerDoc: Accept a NER JSON object and create a graph of the (submitted) file

   iii. Added, GenerateAutoGraph: Accept a list of file names, that will be used to generate the NER generation automatically and create a full graph

8. v0.1.6

   i. Amended, GetGraphRetrieval: to accept optional file reference and base model reference

   ii. Amended, GetGraphRetrievalWithDS: to accept optional file reference and base model reference

9. v0.1.7

   i. Added, GetCustomerGraphRetrievalWithDS: Retrieve customer specific query with the Graph relationships for the requested retrieve query with Graph Node data sets as JSON

10. v0.1.8

   i. Amended, GenerateGraph, GenerateGraphPerDoc & GenerateAutoGraph: to accept graph generation Payload Configuration with the JSON format: {"overrideNER":"<True/False>", "filter":"<GRAPH CASE_TYPE ATTRIBUTE GENERATION CONFIG TEXT>"}

11. v0.1.9

   i. Amended, GetGraphStructure, GetGraphStructurePerDoc, GenerateGraph, GenerateGraphPerDoc & GenerateAutoGraph, to accept the model-id configuration

12. v0.2.0

   i. Added, GetReasoning: Generate Similarity Reasoning of a Solution for a given Sequential Collection Case

13. v0.2.1

   i. Added: tikos.TikosClient, A generic client connector that orchestrates commonly used base functions. It has been developed to facilitate easy integration with other applications and supports multithreading.

   ii. Function: addProcessFiles: Multithreading supported file processing function. Accepts: List of filenames and file paths as a tuple

   iii. Function: addFileStreams: Multithreading supported file addition function. Accepts: List of filenames and file stream as a tuple

   iv. Function: addProcessFileStreams: Multithreading supported combined file addition and processing function. Accepts: List of filenames and file stream as a tuple

   v. Function: generateGraphStructures: Multithreading supported graph structure generation function. Accepts: List of filenames as contexes

   vi. Function: createGraph: Multithreading supported graph creation function. Accepts: List of filenames as contexes

   vii. Function: getGraph: Graph structure extraction function

   viii. Function: getGraphRetrieval: Graph retrieval function, Accepts: Filenames as context and query

   ix. Function: createSequentialCollection: Sequential Collection creation function. Accepts: Case-Type, Data File name as context and Weight Type

   x. Function: generateReasoning: Sequential Collection reasoning function. Accepts: Case-Type, Data File name as context, problem space case as a JSON object string, Weight Type and Reasoning Type

14. v0.2.2

   i. Amended: BuildSC: accepts the Sequential Collection config (scConfig) 

   ii. Amended: tikos.TikosClient.createSequentialCollection: accepts the Sequential Collection config (scConfig)

15. v0.2.3

   i. Function: UploadModel: Upload trained Deep Neural Network model that need to embedded with TRP. PyTorch Based models are supported

   ii. Function: UploadModelConfig: Upload of the configuration related to the Uploaded DNN model. Will accept the model param definition in JSON format as-well-as the model specification in YAML format

   iii. Function: UploadModelCaseData: Upload of the selected Knowledge Cases (feature sets), that will build the initial Sequential Collection case base

   iv. Function: ProcessModel: Process the upload DNN model with Synapses Logger embedding and dynamically creating the Sequential Collection case base

   v. Added: tikos.TikosClient.uploadEmbeddingModel: Supports upload of the DNN model

   vi. Added: tikos.TikosClient.uploadEmbeddingConfig: Supports upload of the DNN model configuration files

   vii. Added: tikos.TikosClient.uploadModelCaseData: Upload of the selected Knowledge Cases (feature sets), that will build the initial Sequential Collection case base

   viii. Added: tikos.TikosClient.processEmbeddedModel: Process the upload DNN model with Synapses Logger embedding and dynamically creating the Sequential Collection case base