function DashboardCard({ title, value, icon }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 flex justify-between items-center">
      <div className="w-3/4">
        <h3 className="text-gray-500 text-sm">
          {title}
        </h3>

        <p className="text-xl font-bold mt-2 break-words">
          {value}
        </p>
      </div>

      <div className="text-4xl text-blue-500">
        {icon}
      </div>
    </div>
  );
}

export default DashboardCard;