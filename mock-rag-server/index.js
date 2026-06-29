const express=require("express");
//now we create a server
const app=express();

//now 
app.use(express.json())

//post sends data while get receives it
app.post("/rag/query", (req, res) => {
    const {question}=req.body;

    setTimeout(() => {
        res.json({
            answer: `This is a mock answer to "${question}"`
        });
    }, 1500);
})

app.listen(8000, ()=> {
    console.log("Mock RAG SERVER IS RUNNING ON PORT 8000");
    
})