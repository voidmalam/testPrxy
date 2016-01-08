Proxy Server <br /> 
1. Create a socket <br /> 
2. Bind socket to a port <br /> 
3. Set socket to listen <br /> 
4. Repeatedly: <br /> 
   a. Accept new connection <---------------- <br /> 
   b. Communicate							              | <br /> 
   c. Close the connection					        | <br /> 
											                      | <br /> 
Client										                  | <br /> 
1. Create a socket  						            | <br /> 
2. Establish connection -------------------- <br /> 
3. Communicate <br /> 
4. Close the connection <br /> 
<br /> 
Proxy server will forward the GET request to the DEMO server with authoraization and event_id. <br /> 
It will receieve JSON formatted event title <br /> 
Proxy server will forward the GET request to the DEMO server with authoraization and event_id. <br /> 
It will receieve JSON formatted event subscription details. <br /> 
<br /> 
Merge these to data in Proxy server and send it back to client program (usually a web browser). <br /> 

To make multiple calls to the proxy server, it should be handled based on thread processing approach.
