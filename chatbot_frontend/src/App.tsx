import {
  MinChatUiProvider,
  MainContainer,
  MessageInput,
  MessageContainer,
  MessageList,
  MessageHeader,
} from "@minchat/react-chat-ui";
import MessageType from "@minchat/react-chat-ui/dist/types/MessageType";
import { useCallback, useEffect, useState } from "react";

function App() {
  const [role, setRole] = useState<"seller" | "customer">("seller");
  const [messages, setMessages] = useState<MessageType[]>([]);

  useEffect(() => {
    setMessages([]);
  }, [role]);

  const handleSendMessage = useCallback(
    (text: string) => {
      setMessages((prv) => [
        ...prv,
        { text, user: { id: "user", name: "You" } },
      ]);
      fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text, type: role }),
      }).then(async (response) => {
        const jsonData = await response.json();

        setMessages((prv) => [
          ...prv,
          { text: jsonData.answer, user: { id: "bot", name: "Bot" } },
        ]);
      });
    },
    [role]
  );

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        flexDirection: "column",
      }}
    >
      <select
        value={role}
        onChange={(e) => setRole(e.target.value as "seller" | "customer")}
        style={{ marginBottom: "20px" }}
      >
        <option value="seller">Seller</option>
        <option value="customer">Customer</option>
      </select>
      <MinChatUiProvider theme="#6ea9d7">
        <MainContainer style={{ height: "800px", width: "500px" }}>
          <MessageContainer>
            <MessageHeader />
            <MessageList currentUserId="dan" messages={messages} />
            <MessageInput
              placeholder="Type message here"
              showSendButton
              onSendMessage={handleSendMessage}
            />
          </MessageContainer>
        </MainContainer>
      </MinChatUiProvider>
    </div>
  );
}

export default App;
