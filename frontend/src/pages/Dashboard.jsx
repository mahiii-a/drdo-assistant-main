import { useEffect, useState } from "react";
import axios from "axios";

import Sidebar from "../components/Sidebar";
import DashboardCard from "../components/DashboardCard";
import RecentActivity from "../components/RecentActivity";
import Navbar from "../components/Navbar";

import { FaFileAlt, FaUpload, FaComments, FaHistory } from "react-icons/fa";

function Dashboard() {
  const [documentsCount, setDocumentsCount] = useState(0);
  const [latestUpload, setLatestUpload] = useState("None");

  const [queryCount, setQueryCount] = useState(0);
  const [activities, setActivities] = useState([]);

  const role = localStorage.getItem("role");

  useEffect(() => {
    fetchDocumentsCount();
    fetchQueryHistory();
  }, []);

  const fetchDocumentsCount = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get("http://localhost:5000/api/documents", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const docs = response.data;

      setDocumentsCount(docs.length);

      if (docs.length > 0) {
        setLatestUpload(docs[0].filename);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const fetchQueryHistory = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://localhost:5000/api/query/history",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      setQueryCount(response.data.length);

      setActivities(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar />

      <main className="flex-1 p-6">
        <Navbar />

        <h1 className="text-3xl font-bold mb-6">
          {role === "admin" ? "Admin Dashboard" : "User Dashboard"}
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <DashboardCard
            title={role === "admin" ? "Total Documents" : "Available Documents"}
            value={documentsCount}
            icon={<FaFileAlt />}
          />

          <DashboardCard
            title={role === "admin" ? "Total Queries" : "My Queries"}
            value={queryCount}
            icon={<FaComments />}
          />

          <DashboardCard
            title={role === "admin" ? "Latest Upload" : "Latest Document"}
            value={
              latestUpload.length > 20
                ? latestUpload.substring(0, 20) + "..."
                : latestUpload
            }
            icon={<FaUpload />}
          />

          <DashboardCard
            title="Recent Activity"
            value={`${queryCount} Activities`}
            icon={<FaHistory />}
          />
        </div>

        <div className="mt-8">
          <RecentActivity />
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
