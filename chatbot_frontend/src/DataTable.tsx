import React from 'react';

interface DataItem {
  [key: string]: any; // Allow any key with any type of value
}

interface DataTableProps {
  data: DataItem[];
}

const DataTable: React.FC<DataTableProps> = ({ data }) => {
  if (data.length === 0) {
    return <div>No data available.</div>; // Handle empty data case
  }

  // Get the headers dynamically from the first item in the data array
  const headers = Object.keys(data[0]);

  return (
    <div style={{ overflowX: 'auto', marginTop: '20px' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {headers.map((header, index) => (
              <th
                key={index}
                style={{ border: '1px solid #ddd', padding: '8px' }}
              >
                {header.charAt(0).toUpperCase() + header.slice(1)}{' '}
                {/* Capitalize header */}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, rowIndex) => (
            <tr key={rowIndex}>
              {headers.map((header, colIndex) => (
                <td
                  key={colIndex}
                  style={{ border: '1px solid #ddd', padding: '8px' }}
                >
                  {item[header] !== null ? item[header] : 'Unknown'}{' '}
                  {/* Display 'Unknown' for null values */}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
