from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from api.models import Proposal, Vote
from api.serializers import ProposalSerializer, VoteSerializer
from api.permissions import IsAdminOrMemberGetPostOnly, IsAdminOrReadOnly

class ProposalListCreateView(generics.ListCreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMemberGetPostOnly]

    def perform_create(self, serializer):
        serializer.save(proposer=self.request.user)


class ProposalVoteView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrMemberGetPostOnly]
    serializer_class = VoteSerializer

    def post(self, request, pk):
        proposal = get_object_or_404(Proposal, pk=pk)

        # Prevent voting on expired or finalized proposals
        if proposal.status != 'pending' or proposal.deadline < timezone.now():
            return Response({"detail": "Voting is closed for this proposal."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(
            data=request.data,
            context={'proposal': proposal, 'user': request.user}
        )
        if serializer.is_valid():
            serializer.save()

            yes_votes, no_votes = proposal.count_votes()

            return Response({
                "detail": "Vote recorded.",
                "yes_votes": yes_votes,
                "no_votes": no_votes,
                "status": proposal.status
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ExpiredProposalsView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        now = timezone.now()
        return Proposal.objects.filter(status='pending', deadline__lt=now)

