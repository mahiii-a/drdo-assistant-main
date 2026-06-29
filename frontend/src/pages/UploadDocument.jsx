import { useState } from "react";
import axios from "axios";
import MainLayout from "../layouts/MainLayout";

function UploadDocument() {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);

  const handleUpload = async (e) => {
  e.preventDefault();

  if (!file) {
    alert("Please select a file");
    return;
  }

  try {
    const formData = new FormData();

    formData.append("document", file);

    const token = localStorage.getItem("token");

    const response = await axios.post(
      "http://localhost:5000/api/documents/upload",
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    alert(response.data.message);

    setTitle("");
    setFile(null);

  } catch (error) {
    console.log(error);

    alert("Upload Failed");
  }
};

  return (
    <MainLayout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">
          Upload Document
        </h1>

        <form
          onSubmit={handleUpload}
          className="bg-white p-6 rounded-lg shadow-md max-w-lg"
        >
          <div className="mb-4">
            <label className="block mb-2 font-semibold">
              Document Title
            </label>

            <input
              type="text"
              value={title}
              onChange={(e) =>
                setTitle(e.target.value)
              }
              className="w-full border p-3 rounded"
              placeholder="Enter document title"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-2 font-semibold">
              Select File
            </label>

            <input
              type="file"
              onChange={(e) =>
                setFile(e.target.files[0])
              }
              className="w-full"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded"
          >
            Upload Document
          </button>
        </form>
      </div>
    </MainLayout>
  );
}

export default UploadDocument;