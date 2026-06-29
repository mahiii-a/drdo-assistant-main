import { useEffect, useState } from "react";
import axios from "axios";

function RecentActivity() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");

    axios
      .get("http://localhost:5000/api/query/history", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setActivities(response.data.slice(0, 5));
      })
      .catch((err) => {
        console.log(err);
        setError(true);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-xl font-bold mb-4">
        Recent Activity
      </h2>

      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Couldn't load recent activity.</p>
      ) : activities.length === 0 ? (
        <p>No activity yet</p>
      ) : (
        <ul className="space-y-3">
          {activities.map((item) => (
            <li key={item.id}>
              ❓ {item.query}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default RecentActivity;