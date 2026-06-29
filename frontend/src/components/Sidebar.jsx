import { Link, useNavigate } from "react-router-dom";
import {
  FaHome,
  FaFileAlt,
  FaUpload,
  FaUser,
  FaSignOutAlt,
  FaComments,
} from "react-icons/fa";

function Sidebar() {
  const role = localStorage.getItem("role");
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");

    navigate("/login");
  };

  return (
    <aside className="w-64 bg-slate-900 text-white min-h-screen">
      <div className="p-6 border-b border-slate-700">
        <h2 className="text-xl font-bold">DRDO Assistant</h2>
      </div>

      <nav className="p-4">
        <ul className="space-y-4">
          <li>
            <Link
              to="/"
              className="flex items-center gap-3 hover:text-blue-400"
            >
              <FaHome />
              Dashboard
            </Link>
          </li>

          {role === "admin" && (
            <>
              <li>
                <Link
                  to="/documents"
                  className="flex items-center gap-3 hover:text-blue-400"
                >
                  <FaFileAlt />
                  Documents
                </Link>
              </li>

              <li>
                <Link
                  to="/upload"
                  className="flex items-center gap-3 hover:text-blue-400"
                >
                  <FaUpload />
                  Upload
                </Link>
              </li>

              <li>
                <Link
                  to="/query"
                  className="flex items-center gap-3 hover:text-blue-400"
                >
                  <FaComments />
                  Query
                </Link>
              </li>
            </>
          )}

          {role === "user" && (
            <li>
              <Link
                to="/query"
                className="flex items-center gap-3 hover:text-blue-400"
              >
                <FaComments />
                Query
              </Link>
            </li>
          )}

          <li>
            <Link
              to="/profile"
              className="flex items-center gap-3 hover:text-blue-400"
            >
              <FaUser />
              Profile
            </Link>
          </li>

          <li
            onClick={handleLogout}
            className="flex items-center gap-3 cursor-pointer hover:text-red-400"
          >
            <FaSignOutAlt />
            Logout
          </li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;
