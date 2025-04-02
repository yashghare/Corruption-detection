import { useEffect, useState } from 'react';

export default function TestConnection() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/test')
      .then(res => res.json())
      .then(data => setData(data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Connection Test</h1>
      {data ? (
        <pre className="bg-gray-100 p-2 mt-2">{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}