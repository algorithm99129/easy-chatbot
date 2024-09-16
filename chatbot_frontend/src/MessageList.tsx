import React from 'react';
import DataTable from './DataTable';
import Chart from './Chart';

interface User {
  id: string;
  name: string;
}

interface Message {
  text?: string;
  user?: User;
  type?: string;
  chartData?: any;
  tableData?: any;
}

interface MessageListProps {
  currentUserId: string;
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({
  currentUserId,
  messages
}) => {
  return (
    <div
      style={{
        flexGrow: 1,
        overflowY: 'auto',
        padding: '12px',
        paddingRight: '24px',
        marginRight: '12px',
        backgroundColor: 'rgb(243, 244, 246)'
      }}
    >
      {messages.map((message, index) => (
        <div
          key={index}
          style={{
            marginBottom: '10px',
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          {message.type === 'table' ? (
            <DataTable data={message.tableData} />
          ) : message.type === 'chart' ? (
            <Chart data={message.chartData} />
          ) : (
            <div
              style={{
                alignSelf: 'start',
                maxWidth: '50%',
                display: 'flex',
                alignItems: 'end',
                columnGap: '4px'
              }}
            >
              <strong style={{ flexBasis: '40px', flexShrink: 0 }}>
                {message.user?.name}:
              </strong>
              <div
                style={{
                  padding: '10px',
                  borderTopLeftRadius: '1px',
                  borderTopRightRadius: '5px',
                  borderBottomLeftRadius: '5px',
                  borderBottomRightRadius: '5px',
                  backgroundColor: 'rgb(110, 169, 215)'
                }}
              >
                {message.text}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default MessageList;
export type { Message };
