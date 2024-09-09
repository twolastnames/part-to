import React, { useState } from "react";
import { JobPost200Body, JobPostBody, doJobPost } from "../api/api.example";
import { useNavigate } from "react-router-dom";

export const JobPost = () => {
  const [text, setText] = useState<string>("");
  const navigate = useNavigate();
  const response = useState<JobPost200Body | undefined>();
  if (!response) {
    return <div>Loading...</div>;
  }
  return (
    <div>
      <textarea
        rows={20}
        cols={60}
        onChange={(input) => {
          setText(input.target.value);
        }}
      ></textarea>
      <button
        onClick={() =>
          doJobPost({
            body: JSON.parse(text) as JobPostBody,
            on200: ({ id }) => {
              navigate(`/job/${id}`);
            },
          })
        }
      >
        Post Job
      </button>
    </div>
  );
};
