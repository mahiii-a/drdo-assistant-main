import { useEffect, useState } from "react";
import axios from "axios";
import MainLayout from "../layouts/MainLayout";

function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://localhost:5000/api/auth/profile",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setUser(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <MainLayout>
      <div className="p-6">
        <h1 className="text-3xl font-bold mb-6">
          Profile
        </h1>

        <div className="bg-white p-6 rounded-lg shadow-md max-w-lg">
          {user ? (
            <>
              <div className="mb-4">
                <p className="font-semibold">Name</p>
                <p>{user.name}</p>
              </div>

              <div className="mb-4">
                <p className="font-semibold">Email</p>
                <p>{user.email}</p>
              </div>

              <div className="mb-4">
                <p className="font-semibold">Role</p>
                <p>{user.role}</p>
              </div>
            </>
          ) : (
            <p>Loading profile...</p>
          )}
        </div>
      </div>
    </MainLayout>
  );
}

export default Profile;