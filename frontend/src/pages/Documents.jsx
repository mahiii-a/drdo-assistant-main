import { useEffect, useState } from "react";
import axios from "axios";
import MainLayout from "../layouts/MainLayout";

function Documents() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://localhost:5000/api/documents",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setDocuments(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const handleDelete = async (id) => {
    try {
      const token = localStorage.getItem("token");

      await axios.delete(
        `http://localhost:5000/api/documents/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert("Document deleted successfully");

      fetchDocuments();
    } catch (error) {
      console.log(error);

      alert("Delete failed");
    }
  };

  return (
    <MainLayout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">
          Documents
        </h1>

        <div className="bg-white rounded-lg shadow-md p-6">
          {documents.length === 0 ? (
            <p>No documents uploaded yet.</p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">
                    File Name
                  </th>

                  <th className="text-left p-2">
                    File Type
                  </th>

                  <th className="text-left p-2">
                    Upload Date
                  </th>

                  <th className="text-left p-2">
                    Action
                  </th>
                </tr>
              </thead>

              <tbody>
                {documents.map((doc) => (
                  <tr
                    key={doc.id}
                    className="border-b"
                  >
                    <td className="p-2">
                      {doc.filename}
                    </td>

                    <td className="p-2">
                      {doc.filetype}
                    </td>

                    <td className="p-2">
                      {new Date(
                        doc.upload_date
                      ).toLocaleDateString()}
                    </td>

                    <td className="p-2">
                      <button
                        onClick={() =>
                          handleDelete(doc.id)
                        }
                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </MainLayout>
  );
}

export default Documents;