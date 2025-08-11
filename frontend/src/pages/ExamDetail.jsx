import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";

export default function ExamDetail() {
  const { id } = useParams();
  const [exam, setExam] = useState(null);

  useEffect(() => {
    api.get(`/exam/exams/${id}/`)
      .then(res => setExam(res.data))
      .catch(err => console.error(err));
  }, [id]);

  if (!exam) return <p>Loading...</p>;

  return (
    <div style={{ maxWidth: 600, margin: "auto" }}>
      <h1>{exam.title}</h1>
      <p><strong>Description:</strong> {exam.description}</p>
      <p><strong>Type:</strong> {exam.exam_type_display}</p>
      <p><strong>Duration:</strong> {exam.duration} minutes</p>
      <p><strong>Price:</strong> ${exam.price}</p>
      <p><strong>Questions:</strong> {exam.question_count}</p>
      <p><strong>Created By:</strong> {exam.created_by_username}</p>
      <p><strong>Created At:</strong> {new Date(exam.created_at).toLocaleString()}</p>
    </div>
  );
}
